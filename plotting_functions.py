import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from scipy import stats


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


def diameters_plot(file_path, title, show_plot=False, save_plot=False):
    # Read data from file
    locations = []
    values = []
    with open(file_path, 'r') as f:
        for line in f:
            location, value = line.split(': ')
            locations.append(location)
            values.append(float(value))

    # Create plot
    plt.bar(locations, values)
    plt.xlabel('Location')
    plt.ylabel('Value')
    plt.title(title)
    plt.yticks(fontsize=14)
    plt.xticks(rotation=90, fontsize=14)

    # Save and/or show the plot
    if save_plot:
        save_path = file_path.replace('.txt', '.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    if show_plot:
        plt.show()
    else:
        plt.close()


def modularity_plot(data_lists, x_labels, y_labels, title=None, save_path=None, show=True):
    fig = px.scatter()
    for i, data_list in enumerate(data_lists):
        fig.add_scatter(x=x_labels, y=data_list, name=y_labels[i])
    fig.update_layout(title=title, xaxis_title="locations", yaxis_title="modularity")
    if save_path:
        fig.write_image(save_path)
    if show:
        fig.show()
    return fig


def modularity_bootstrap_plot(Q, dictionary, x_labels, title='bootstrap plot', save_path=None, show=True):
    for key, value in dictionary.items():
        data_lists = [Q, value['mode']]
        y_labels = ['Q', 'Q_sampled_' + str(key)]
        fig = modularity_plot(data_lists, x_labels, y_labels, title=title, save_path=None, show=False)
        fig.add_trace(go.Scatter(x=x_labels + x_labels[::-1], y=value['max'] + value['min'][::-1], fill='toself', fillcolor='rgba(0,100,80,0.2)', line=dict(color='rgba(255, 255, 255, 0)'), showlegend=False))

        if save_path:
            fig.write_image(save_path[:-4] + "_" + str(key) + '.png')

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


def test_modularity_bootstrap_plot():
    # Generate sample data
    dict_data = {
        'A': np.random.normal(loc=10, scale=1, size=100),
        'B': np.random.normal(loc=20, scale=3, size=100),
        'C': np.random.normal(loc=15, scale=2, size=100)
    }

    # Call plot function
    modularity_bootstrap_plot(dict_data, title='Sample Data', x_axis_label='Groups', y_axis_label='Values')


def main():
    test_radial_graph_plot()
    test_matrix_plot()


if __name__ == "__main__":
    main()
