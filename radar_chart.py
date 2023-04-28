import plotly.graph_objects as go


def radial_graph_plot(vals_dict, theta, title, filename, save=True):
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

    fig.show()


def main():
    theta = ['Fats', 'Proteins', 'Carbs', 'Fiber', 'Sugar']
    filename = 'figures/test.png'
    title = 'Title!'
    vals = {'f1': [0.18, 0.06, 0.39, 0.36, 0],
            'f2': [0.43, 0.08, 0.3, 0.08, 0.1],
            'f3': [0.08, 0.23, 0.58, 0.1, 0.01],
            'f4': [0.13, 0.2, 0.54, 0.12, 0.02]}
    radial_graph_plot(vals, theta, title, filename, save=True)


if __name__=="__main__":
    main()
