from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

f = plt.figure(figsize=(8, 8))


# 接受一个时间参数，
def make_frame_mpl(t):
    ...
    return mplfig_to_npimage(f)
    # 所有的图像都在同一个figure上

animation = mpy.VideoClip(make_frame_mpl, duration=5)
animation.write_gif("animation-94a2c1ff.gif", fps=20)
