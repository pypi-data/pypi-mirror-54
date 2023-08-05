import functools
import math
import os
import random
from hashlib import md5, sha1
from pathlib import Path

import pendulum
from colorama import Fore
from sortedcontainers import SortedDict
from tbm_utils import humanize_filesize
from tqdm import tqdm

from . import bencode
from .config import CONFIG_PATH
from .constants import DEFAULT_ABBRS
from .utils import (
	calculate_torrent_size,
	generate_unique_string,
	get_file_path,
	hash_info_dict,
)

tqdm.format_sizeof = functools.partial(humanize_filesize, precision=2)


def create_dir_info_dict(
	filepaths,
	data_size,
	piece_size,
	private,
	source,
	include_md5,
	show_progress=True,
):
	base_path = Path(os.path.commonpath(filepaths))

	info_dict = SortedDict()
	file_infos = []
	data = bytes()
	pieces = bytes()

	if show_progress:
		print("\n")
		progress_bar = tqdm(
			total=data_size,
			unit='',
			unit_scale=True,
			leave=True,
			dynamic_ncols=True,
			bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} [{remaining} {rate_fmt}]',
		)

	for filepath in filepaths:
		file_dict = SortedDict()
		length = 0

		md5sum = md5() if include_md5 else None

		with open(filepath, 'rb') as f:
			while True:
				piece = f.read(piece_size)

				if not piece:
					break

				length += len(piece)

				data += piece

				if len(data) >= piece_size:
					pieces += sha1(data[:piece_size]).digest()
					data = data[piece_size:]

				if include_md5:
					md5sum.update(piece)

				if show_progress:
					progress_bar.update(len(piece))

		file_dict['length'] = length
		file_dict['path'] = get_file_path(filepath, base_path)

		if include_md5:
			file_dict['md5sum'] = md5sum.hexdigest()

		file_infos.append(file_dict)

	if show_progress:
		progress_bar.close()

	if len(data) > 0:
		pieces += sha1(data).digest()

	info_dict['files'] = file_infos
	info_dict['name'] = base_path.name
	info_dict['pieces'] = pieces
	info_dict['piece length'] = piece_size
	info_dict['salt'] = generate_unique_string()

	info_dict['private'] = 1 if private else 0

	if source:
		info_dict['source'] = source

	return info_dict


def create_file_info_dict(
	filepaths,
	data_size,
	piece_size,
	private,
	source,
	include_md5,
	show_progress=True,
):
	info_dict = SortedDict()
	pieces = bytes()
	length = 0

	md5sum = md5() if include_md5 else None

	if show_progress:
		print("\n")
		progress_bar = tqdm(
			total=data_size,
			unit='',
			unit_scale=True,
			leave=True,
			dynamic_ncols=True,
			bar_format='{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt} [{remaining} {rate_fmt}]',
		)

	with open(filepaths[0], 'rb') as f:
		while True:
			piece = f.read(piece_size)

			if not piece:
				break

			length += len(piece)

			pieces += sha1(piece).digest()

			if include_md5:
				md5sum.update(piece)

			if show_progress:
				progress_bar.update(len(piece))

	if show_progress:
		progress_bar.close()

	info_dict['name'] = filepaths[0].name
	info_dict['length'] = length
	info_dict['pieces'] = pieces
	info_dict['piece length'] = piece_size
	info_dict['salt'] = generate_unique_string()

	info_dict['private'] = 1 if private else 0

	if source:
		info_dict['source'] = source

	if include_md5:
		info_dict['md5sum'] = md5sum.hexdigest()

	return info_dict


def generate_magnet_link(torrent_info):
	torrent_name = torrent_info['info']['name']
	info_hash = hash_info_dict(torrent_info['info'])
	data_size = calculate_torrent_size(torrent_info)

	magnet_link = f'magnet:?dn={torrent_name}&xt=urn:btih:{info_hash}&xl={data_size}'

	if 'announce-list' in torrent_info:
		for tier in torrent_info['announce-list']:
			magnet_link += f'&tr={random.choice(tier)}'
	elif 'announce' in torrent_info:
		magnet_link += f'&tr={torrent_info["announce"]}'

	return magnet_link


def output_abbreviations(conf):
	def abbr_list(abbrs):
		lines = []
		for abbr, tracker in abbrs.items():
			if isinstance(tracker, list):
				line = f'{Fore.CYAN}{abbr}: ' + '\n'.ljust(23).join(
					f'{Fore.MAGENTA}{track}'
					for track in tracker
				)
			else:
				line = f'{Fore.CYAN}{abbr}: {Fore.MAGENTA}{tracker}'

			lines.append(line)

		return '\n'.ljust(17).join(lines)

	auto_abbrs = abbr_list(
		{
			'open': "All default trackers in a random tiered order.",
			'random': "A single random default tracker.",
		}
	)
	default_abbrs = abbr_list(
		{
			abbr: tracker
			for abbr, tracker in DEFAULT_ABBRS.items()
			if abbr not in ['open', 'random']
		}
	)
	user_abbrs = abbr_list(conf['trackers'])

	summary = (
		f"\n"
		f"{Fore.YELLOW}{'Config File'}:    {Fore.CYAN}{CONFIG_PATH}\n\n"
		f"{Fore.YELLOW}{'Auto'}:           {auto_abbrs}\n\n"
		f"{Fore.YELLOW}{'Default'}:        {default_abbrs}\n\n"
		f"{Fore.YELLOW}{'User'}:           {user_abbrs}"
	)

	print(summary)


def output_summary(torrent_info, show_files=False):
	torrent_name = torrent_info['info']['name']
	info_hash = hash_info_dict(torrent_info['info'])
	private = 'Yes' if torrent_info['info'].get('private') == 1 else 'No'

	announce_list = None
	if 'announce-list' in torrent_info:
		announce_list = torrent_info['announce-list']
	elif 'announce' in torrent_info:
		announce_list = [[torrent_info['announce']]]

	if announce_list:
		tracker_list = '\n\n'.ljust(18).join(
			'\n'.ljust(17).join(
				tracker
				for tracker in tier
			)
			for tier in announce_list
		)
	else:
		tracker_list = None

	data_size = calculate_torrent_size(torrent_info)
	piece_size = torrent_info['info']['piece length']
	piece_count = math.ceil(data_size / piece_size)

	tz = pendulum.tz.local_timezone()
	creation_date = pendulum.from_timestamp(
		torrent_info['creation date'],
		tz
	).format('YYYY-MM-DD HH:mm:ss Z')
	created_by = torrent_info.get('created by', '')
	comment = torrent_info.get('comment', '')
	source = torrent_info.get('source', '')

	magnet_link = generate_magnet_link(torrent_info)

	summary = (
		f"\n"
		f"{Fore.YELLOW}{'Info Hash'}:      {Fore.CYAN}{info_hash}\n"
		f"{Fore.YELLOW}{'Torrent Name'}:   {Fore.CYAN}{torrent_name}\n"
		f"{Fore.YELLOW}{'Data Size'}:      {Fore.CYAN}{humanize_filesize(data_size, precision=2)}\n"
		f"{Fore.YELLOW}{'Piece Size'}:     {Fore.CYAN}{humanize_filesize(piece_size)}\n"
		f"{Fore.YELLOW}{'Piece Count'}:    {Fore.CYAN}{piece_count}\n"
		f"{Fore.YELLOW}{'Private'}:        {Fore.CYAN}{private}\n"
		f"{Fore.YELLOW}{'Creation Date'}:  {Fore.CYAN}{creation_date}\n"
		f"{Fore.YELLOW}{'Created By'}:     {Fore.CYAN}{created_by}\n"
		f"{Fore.YELLOW}{'Comment'}:        {Fore.CYAN}{comment}\n"
		f"{Fore.YELLOW}{'Source'}:         {Fore.CYAN}{source}\n"
		f"{Fore.YELLOW}{'Trackers'}:       {Fore.CYAN}{tracker_list}\n\n"
		f"{Fore.YELLOW}{'Magnet'}:         {Fore.CYAN}{magnet_link}"
	)

	if show_files:
		file_infos = []
		if 'files' in torrent_info['info']:
			for f in torrent_info['info']['files']:
				file_infos.append(
					(
						humanize_filesize(f['length'], precision=2),
						Path(*f['path']),
					)
				)
		else:
			file_infos.append(
				(
					humanize_filesize(
						torrent_info['info']['length'], precision=2
					),
					Path(torrent_info['info']['name']),
				)
			)

		pad = len(
			max(
				(size for size, _ in file_infos),
				key=len
			)
		)

		summary += f"\n\n{Fore.YELLOW}{'Files'}:\n\n"
		for size, path in file_infos:
			summary += f"    {Fore.WHITE}{f'{size:<{pad}}'}  {Fore.GREEN}{path}\n"

	print(summary)


def read_torrent_file(filepath):
	try:
		torrent_info = bencode.load(filepath.open('rb'))
	except FileNotFoundError:
		raise FileNotFoundError(f"{filepath} not found.")
	except TypeError:
		raise TypeError(f"Could not parse {filepath}.")

	return torrent_info


def write_torrent_file(filepath, torrent_info):
	bencode.dump(torrent_info, filepath.open('wb'))
