import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import widgets
import itkwidgets
import itk
from scipy.signal import stft
from pynwb.ecephys import LFP
from .base import fig2widget


def show_lfp(node: LFP, **kwargs):
    #lfp = node.electrical_series['ElectricalSeries']
    lfp = list(node.electrical_series.values())[0]
    ntabs = 3
    children = [widgets.HTML('Rendering...') for _ in range(ntabs)]

    def on_selected_index(change):
        # Click on Traces Tab
        if change.new == 1 and isinstance(change.owner.children[1], widgets.HTML):
            widget_box = show_voltage_traces(lfp)
            children[1] = widget_box
            change.owner.children = children

        # Click on Spectrogram Tab
        if change.new == 2 and isinstance(change.owner.children[1], widgets.HTML):
            #slider = widgets.IntSlider(value=0, min=0, max=lfp.data.shape[1] - 1, description='Channel',
            #                           orientation='horizontal')
            ch = widgets.BoundedIntText(value=0, min=0, max=lfp.data.shape[1] - 1,
                                        description='Channel', continuous_update=False)

            def create_spectrogram(channel=0):
                f, t, Zxx = stft(lfp.data[:, channel], lfp.rate, nperseg=128)
                spect = np.log(np.abs(Zxx))
                image = itk.GetImageFromArray(spect)
                image.SetSpacing([(f[1] - f[0]), (t[1] - t[0]) * 1e-1])
                direction = image.GetDirection()
                vnl_matrix = direction.GetVnlMatrix()
                vnl_matrix.set(0, 0, 0.0)
                vnl_matrix.set(0, 1, -1.0)
                vnl_matrix.set(1, 0, 1.0)
                vnl_matrix.set(1, 1, 0.0)
                return image

            spectrogram = create_spectrogram(0)

            viewer = itkwidgets.view(spectrogram, ui_collapsed=True, select_roi=True, annotations=False)
            spect_vbox = widgets.VBox([ch, viewer])
            children[2] = spect_vbox
            change.owner.children = children
            channel_to_spectrogram = {0: spectrogram}

            def on_change_channel(change):
                channel = change.new
                if channel not in channel_to_spectrogram:
                    channel_to_spectrogram[channel] = create_spectrogram(channel)
                viewer.image = channel_to_spectrogram[channel]

            ch.observe(on_change_channel, names='value')

    vbox = []
    for key, value in lfp.fields.items():
        vbox.append(widgets.Text(value=repr(value), description=key, disabled=True))
    children[0] = widgets.VBox(vbox)

    tab_nest = widgets.Tab()
    # Use Rendering... as a placeholder
    tab_nest.children = children
    tab_nest.set_title(0, 'Fields')
    tab_nest.set_title(1, 'Traces')
    tab_nest.set_title(2, 'Spectrogram')
    tab_nest.observe(on_selected_index, names='selected_index')
    return tab_nest


def show_voltage_traces(lfp):
    # Produce figure
    def control_plot(x0, x1, ch0, ch1):
        fig, ax = plt.subplots(figsize=(18, 10))
        data = lfp.data[x0:x1, ch0:ch1+1]
        xx = np.arange(x0, x1)
        mu_array = np.mean(data, 0)
        sd_array = np.std(data, 0)
        offset = np.mean(sd_array)*5
        yticks = [i*offset for i in range(ch1+1-ch0)]
        for i in range(ch1+1-ch0):
            ax.plot(xx, data[:, i] - mu_array[i] + yticks[i])
        ax.set_xlabel('Time [ms]', fontsize=20)
        ax.set_ylabel('Ch #', fontsize=20)
        ax.set_yticks(yticks)
        ax.set_yticklabels([str(i) for i in range(ch0, ch1+1)])
        ax.tick_params(axis='both', which='major', labelsize=16)
        plt.show()
        return fig2widget(fig)

    fs = lfp.rate
    nSamples = lfp.data.shape[0]
    nChannels = lfp.data.shape[1]

    # Controls
    field_lay = widgets.Layout(max_height='40px', max_width='100px',
                               min_height='30px', min_width='70px')
    x0 = widgets.BoundedIntText(value=0, min=0, max=int(1000*nSamples/fs-100),
                                layout=field_lay)
    x1 = widgets.BoundedIntText(value=10000, min=100, max=int(1000*nSamples/fs),
                                layout=field_lay)
    ch0 = widgets.BoundedIntText(value=0, min=0, max=int(nChannels-1), layout=field_lay)
    ch1 = widgets.BoundedIntText(value=10, min=0, max=int(nChannels-1), layout=field_lay)

    controls = {
        'x0': x0,
        'x1': x1,
        'ch0': ch0,
        'ch1': ch1
    }
    out_fig = widgets.interactive_output(control_plot, controls)

    # Assemble layout box
    lbl_x = widgets.Label('Time [ms]:', layout=field_lay)
    lbl_ch = widgets.Label('Ch #:', layout=field_lay)
    lbl_blank = widgets.Label('    ', layout=field_lay)
    hbox0 = widgets.HBox(children=[lbl_x, x0, x1, lbl_blank, lbl_ch, ch0, ch1])
    vbox = widgets.VBox(children=[hbox0, out_fig])
    return vbox


def show_spectrogram(neurodata, channel=0, **kwargs):
    fig, ax = plt.subplots()
    f, t, Zxx = stft(neurodata.data[:, channel], neurodata.rate, nperseg=2*17)
    ax.imshow(np.log(np.abs(Zxx)), aspect='auto', extent=[0, max(t), 0, max(f)], origin='lower')
    ax.set_ylim(0, 50)
    ax.set_xlabel('time')
    ax.set_ylabel('frequency')
    plt.show(ax.figure())


def show_spike_event_series(ses, **kwargs):
    def control_plot(spk_ind):
        fig, ax = plt.subplots()
        data = ses.data[spk_ind, :, :]
        for ch in range(nChannels):
            ax.plot(data[:, ch], color='#d9d9d9')
        ax.plot(np.mean(data, axis=1), color='k')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        plt.show()
        return view.fig2widget(fig)

    nChannels = ses.data.shape[2]
    nSpikes = ses.data.shape[0]

    # Controls
    field_lay = widgets.Layout(max_height='40px', max_width='100px',
                               min_height='30px', min_width='70px')
    spk_ind = widgets.BoundedIntText(value=0, min=0, max=nSpikes-1,
                                     layout=field_lay)
    controls = {'spk_ind': spk_ind}
    out_fig = widgets.interactive_output(control_plot, controls)

    # Assemble layout box
    lbl_spk = widgets.Label('Spike ID:', layout=field_lay)
    lbl_nspks0 = widgets.Label('N° spikes:', layout=field_lay)
    lbl_nspks1 = widgets.Label(str(nSpikes), layout=field_lay)
    lbl_nch0 = widgets.Label('N° channels:', layout=field_lay)
    lbl_nch1 = widgets.Label(str(nChannels), layout=field_lay)
    hbox0 = widgets.HBox(children=[lbl_spk, spk_ind])
    vbox0 = widgets.VBox(children=[
        widgets.HBox(children=[lbl_nspks0, lbl_nspks1]),
        widgets.HBox(children=[lbl_nch0, lbl_nch1]),
        hbox0
    ])
    hbox1 = widgets.HBox(children=[vbox0, out_fig])

    return hbox1
