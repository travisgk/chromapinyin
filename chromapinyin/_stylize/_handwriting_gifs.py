import os
import time
from ._res_directories import get_handwriting_path, get_handwriting_gifs_path
_process_possible = True
try:
	import imageio.v3 as imageio
except:
	_process_possible = False
import PIL
import numpy as np

# the animations have their speed adjusted
# <n_anim_speeds> will specify how many different animation speeds should be used.
# this has the effect of letting GIFs be sychronized.
# for example, a really complex hanzi will loop 1 time,
# but the demonstration of a simple hanzi will loop 5 times in that time span.
def process_gifs(
	min_anim_ms= 3000,
	start_freeze_ms=1500,
	end_freeze_ms=3500,
	loops=True,
	n_anim_speeds=5
):
	if not _process_possible:
		print("processing GIFs is not possible. imageio was not found.")
		print("run 'pip install imageio' to use the process_gifs() function.")
		return

	print("Beginning processing GIFs.")
	start_time = time.time()
	handwriting_dir = get_handwriting_gifs_path()
	large_handwriting_dir = os.path.join(get_handwriting_path(), "images-large")

	process_normal_gifs = os.path.exists(handwriting_dir)
	process_large_gifs = os.path.exists(large_handwriting_dir)

	n_files = 0

	if not process_normal_gifs:
		print(f"{handwriting_dir} could not be found.")
	else:
		file_names = os.listdir(handwriting_dir)
		n_files = len(file_names)
		if process_large_gifs:
			n_files = n_files * 2

		for i, file_name in enumerate(file_names):
			gif_path = os.path.join(handwriting_dir, file_name)
			_modify_gif(
				gif_path,
				min_anim_ms,
				start_freeze_ms,
				end_freeze_ms,
				loops,
				n_anim_speeds
			)

			if (i + 1) % 100 == 0:
				elapsed = time.time() - start_time
				h, m, s = _estimated_time_remaining(i + 1, n_files, elapsed)
				print(f"{i+1:>5d} / {n_files:>5d}\t{h:>2d}:{m:02d}:{s:02d}")

	if not os.path.exists(large_handwriting_dir):
		print(f"{large_handwriting_dir} could not be found.")
	else:
		file_names = os.listdir(large_handwriting_dir)
		i_offset = len(file_names)
		if not process_normal_gifs:
			i_offset = 0
			n_files = len(file_names)

		for i, file_name in enumerate(file_names):
			gif_path = os.path.join(large_handwriting_dir, file_name)
			_modify_gif(
				gif_path,
				min_anim_ms,
				start_freeze_ms,
				end_freeze_ms,
				loops,
				n_anim_speeds
			)
			new_gif_path = os.path.join(
				large_handwriting_dir, file_name.replace("-large", "")
			)
			os.rename(gif_path, new_gif_path)

			current_i = i + i_offset + 1
			if current_i % 100 == 0:
				elapsed = time.time() - start_time
				h, m, s = _estimated_time_remaining(current_i, n_files, elapsed)
				print(f"{current_i:>5d} / {n_files:>5d}\t{h:>2d}:{m:02d}:{s:02d}")

# returns hours, minutes, seconds of the estimated time remaining.
def _estimated_time_remaining(i, n_files, elapsed_time):
	time_per_iteration = elapsed_time / i
	n_remaining = n_files - i
	time_remaining = n_remaining * time_per_iteration
	seconds = int(time_remaining)
	hours = seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60
	return hours, minutes, seconds

# overwrites the GIF image at <gif_path> to change its speed
# and whether it loops or not.
def _modify_gif(
	gif_path,
	min_anim_ms,
	start_freeze_ms,
	end_freeze_ms,
	loops,
	n_anim_speeds
):
	try:
		im_gif = PIL.Image.open(gif_path)
	except PIL.UnidentifiedImageError:
		print(f"{gif_path} cannot be identified by PIL.")
		return

	MIN_N_FRAMES =  12
	MAX_N_FRAMES = 105
	frames = []
	for i, frame in enumerate(_iter_frames(im_gif)):
		frames.append(np.array(frame, dtype=np.uint8))

	n_frames = len(frames)
	standard_delay = min_anim_ms // MIN_N_FRAMES
	max_anim_ms = standard_delay * MAX_N_FRAMES

	print(f"n_frames: {n_frames}, min: {min_anim_ms}, max: {max_anim_ms}") # DEBUG

	offset_ms = (max_anim_ms - min_anim_ms) // (n_anim_speeds - 1)

	
	anim_ms = 1
	selection = 0
	for i in range(n_anim_speeds):
		threshold = MIN_N_FRAMES + (i + 1) * (
			(MAX_N_FRAMES - MIN_N_FRAMES) // n_anim_speeds
		)
		if n_frames < threshold:
			selection = i
			anim_ms = min_anim_ms + i * offset_ms
			break
	print(f"{n_frames}: {anim_ms}") # DEBUG

	frame_delay_ms = int(anim_ms / n_frames)
	leftover_ms = anim_ms - (frame_delay_ms * n_frames)

	durations = [frame_delay_ms for _ in range(len(frames))]
	durations[0] = start_freeze_ms
	durations[-1] = end_freeze_ms + leftover_ms

	# duration is the time (in ms) that a frame is shown. If you pass an int it will
	# be the same for each frame, if you pass a list (or iterable) it can be set on
	# a per-frame basis.
	imageio.imwrite(gif_path, frames, duration=durations, loop=0 if loops else 1)

# iterates and yields each individual frame of the given PIL .gif image.
def _iter_frames(im_gif):
	try:
		i = 0
		while True:
			im_gif.seek(i)
			im_frame = im_gif.convert("RGBA")
			yield im_frame
			i += 1
	except EOFError:
		pass

