import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def radial_graph_plot(vals_dict, theta, title, filename, save=True, show=False):
    fig = go.Figure()

    for name, vals in vals_dict.items():
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=theta,
            fill='toself',
            name=name,
            # opacity=0.5
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=dict(
            text=title,
            x=0.5,
            y=0.95
        ),
    )

    if save:
        fig.write_image(filename)
    if show:
        fig.show()


def matrix_plot(vals, diag_vals, labels, title, filename, save=True, show=False):
    """
    Assumes that vals correspond to using the "itertools" combinations function on nutrients
    """
    num_nutrients = len(labels)
    mat = np.zeros([num_nutrients, num_nutrients]) + np.nan

    k = 0
    for i in range(num_nutrients):
        for j in range(i+1, num_nutrients):
            mat[i, j] = vals[k]
            k += 1
    for i in range(num_nutrients):
        mat[i, i] = diag_vals[i]

    mat = mat.T

    fig = px.imshow(mat, x=labels, y=labels, color_continuous_scale='ice')
    fig.update_layout(title_text=title, title_x=0.5)
    if save:
        fig.write_image(filename)
    if show:
        fig.show()


# ########## #
# Test cases #
# ########## #
def test_radial_graph_plot():
    theta = ['Fats', 'Proteins', 'Carbs', 'Fiber', 'Sugar']
    filename = 'figures/test_radar.png'
    title = 'Title!'
    vals = {'f1': [0.18, 0.06, 0.39, 0.36, 0],
            'f2': [0.43, 0.08, 0.3, 0.08, 0.1],
            'f3': [0.08, 0.23, 0.58, 0.1, 0.01],
            'f4': [0.13, 0.2, 0.54, 0.12, 0.02]}
    radial_graph_plot(vals, theta, title, filename, save=True)


def test_matrix_plot():
    theta = ['Fats', 'Proteins', 'Carbs']
    filename = 'figures/test_matrix.png'
    title = 'Title!'
    vals = [0.1, 0.2, 0.3]
    diag_vals = [0, 0.05, 0.1]
    matrix_plot(vals, diag_vals, theta, title, filename, save=True)


def main():
    test_radial_graph_plot()
    test_matrix_plot()


if __name__ == "__main__":
    main()
