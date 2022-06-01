import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mplcolors

import argparse

def lorenz(x, y, z, r, s, b):
    """
    Given:
       x, y, z: a point of interest in three dimensional space
       s, r, b: parameters defining the lorenz attractor
    Returns:
       x_dot, y_dot, z_dot: values of the lorenz attractor's partial
           derivatives at the point x, y, z
    """
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot

dt = 0.005

xs = []
ys = []
zs = []

x = []
y = []
z = []

# Uncomment for a multicolored line animation
#lines = []

ANGLE_INCREMENTS = 0.5
LINE_WIDTH = 1

def animate(i):
    x.append(xs[i])
    y.append(ys[i])
    z.append(zs[i])

    norm = mplcolors.Normalize(xs.min(), xs.max())
    m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
    # Multi-colored line hack / slows down the animation
    #line, = ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=m.to_rgba(xs[i]), lw=LINE_WIDTH)
    #lines.append(line)
    #return tuple(lines) + (point,)

    line, = ax.plot(x, y, z, color='orange', lw=LINE_WIDTH)
    point, = ax.plot(xs[i], ys[i], zs[i], marker='o', markersize=4, color='red')

    return line,point,


def init_data(frame_count, r, s, b):
    global fig
    global ax
    global xs
    global ys
    global zs

    plt.style.use('dark_background')
    num_steps = frame_count
    # Need one more for the initial values
    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)

    # Set initial values
    xs[0], ys[0], zs[0] = (0., 1., 1.05)
    for i in range(num_steps):
        x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i], r, s, b)
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)

    # Plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(projection='3d')
    #fig.tight_layout()

    ax.set_zlim([-10, 50])
    ax.set_xlim([-30, 30])
    ax.set_ylim([-30, 30])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Lorenz Attractor\n[ρ = {r}, σ = {s}, β = {b}]", fontsize=16)

    # Navy panes
    pane_color = (8/256, 14/256, 44/256, 0.5)
    ax.w_xaxis.set_pane_color(pane_color)
    ax.w_yaxis.set_pane_color(pane_color)
    ax.w_zaxis.set_pane_color(pane_color)
    #Hide all axes
    #ax.set_axis_off()
    #Hide grid
    #ax.grid(False)
    #Hide Z axis
    #ax.w_zaxis.line.set_lw(0.)
    #ax.set_zticks([])


def main():

    parser = argparse.ArgumentParser(description='Plot Lorenz Attractor')


    parser.add_argument('-n','--steps', help='Frame/step count to simulate', default = 10000, type = int, metavar = '')
    parser.add_argument('-r','--ro', help='ρ value of attractor', default = 28, type = int, metavar = '')
    parser.add_argument('-s','--sigma', help='σ value of attractor', default = 10, type = int, metavar = '')
    parser.add_argument('-b','--beta', help='β value of attractor', default = round(8/3, 3), type = float, metavar = '')
    # Either animate or create frames
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-a','--animate', help='Animate flag', action ='store_true')
    group.add_argument('-f','--frames', help='Save frames flag', action ='store_true')

    args = vars(parser.parse_args())
    animate_flag = args['animate']
    save_frames = args['frames']
    frame_count = args['steps']
    # Lorenz attractor parameters
    r = args['ro']
    s = args['sigma']
    b = args['beta']

    init_data(frame_count, r, s, b)

    if animate_flag:
        anim = animation.FuncAnimation(fig, animate, frames=frame_count, interval=1, blit=True, repeat = False)
        plt.show()
    elif save_frames:
        norm = mplcolors.Normalize(xs.min(), xs.max())
        m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
        azim = -60 #Initial azimuth angle
        for i in range(frame_count):
            ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], color=m.to_rgba(xs[i]), lw=LINE_WIDTH)
            dot, = ax.plot(xs[i+1], ys[i+1], zs[i+1], marker='o', markersize=4, color='red')
            plt.savefig(f'frames/{i}.png', dpi = 300)
            dot.remove()
            # For a rotating view around Z axis
            azim += ANGLE_INCREMENTS
            ax.view_init(azim=azim, elev=30)
    else:
        norm = mplcolors.Normalize(xs.min(), xs.max())
        m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
        for i in range(frame_count):
            ax.plot(xs[i:i+2], ys[i:i+2], zs[i:i+2], color=m.to_rgba(xs[i]), lw=LINE_WIDTH)
        ax.plot(xs[-1], ys[-1], zs[-1], marker='o', markersize=4, color='red')
        plt.show()


if __name__ == "__main__":
    main()
