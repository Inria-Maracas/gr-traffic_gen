#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulated Traffic Generator
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import traffic_gen
from gnuradio import qtgui

class modulated_traffic_gen(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulated Traffic Generator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulated Traffic Generator")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "modulated_traffic_gen")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tag_length = tag_length = "traffic_length"
        self.samp_rate = samp_rate = 32000
        self.qam64 = qam64 = digital.qam.qam_constellation(constellation_points=64, differential=True, mod_code='none', large_ampls_to_corners=False)
        self.qam256 = qam256 = digital.qam.qam_constellation(constellation_points=256, differential=True, mod_code='none', large_ampls_to_corners=False)
        self.qam16 = qam16 = digital.qam.qam_constellation(constellation_points=16, differential=True, mod_code='none', large_ampls_to_corners=False)
        self.psk8 = psk8 = digital.psk.psk_constellation(m=8, mod_code='none', differential=True)
        self.psk4 = psk4 = digital.psk.psk_constellation(m=4, mod_code='none', differential=True)
        self.psk2 = psk2 = digital.psk.psk_constellation(m=2, mod_code='none', differential=True)
        self.margin = margin = 3000
        self.const_QAM16 = const_QAM16 = digital.constellation_16qam().base()

        ##################################################
        # Blocks
        ##################################################
        self.traffic_gen_trigger_0 = traffic_gen.trigger('127.0.0.1', 7000, tag_length, margin)
        self.traffic_gen_mmse_resampler_cc_0 = traffic_gen.mmse_resampler_cc(0, 1)
        self.traffic_gen_margin_cut_0 = traffic_gen.margin_cut(margin, margin, tag_length, True)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
            samples_per_symbol=2,
            bt=0.35,
            verbose=False,
            log=False)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(const_QAM16.points(), 1)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.complex_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.complex_t, 'packet_len')
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.blocks_int_to_float_0_0_0 = blocks.int_to_float(1, 1)
        self.blocks_int_to_float_0_0 = blocks.int_to_float(1, 1)
        self.blocks_int_to_float_0 = blocks.int_to_float(1, 1)
        self.analog_random_source_x_0_1 = blocks.vector_source_i(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_random_source_x_0_0_0 = blocks.vector_source_i(list(map(int, numpy.random.randint(0, 4, 1000))), True)
        self.analog_random_source_x_0_0 = blocks.vector_source_i(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc(1)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_magphase_to_complex_0, 1))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.blocks_null_sink_0_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.blocks_int_to_float_0, 0))
        self.connect((self.analog_random_source_x_0_0_0, 0), (self.blocks_int_to_float_0_0, 0))
        self.connect((self.analog_random_source_x_0_1, 0), (self.blocks_int_to_float_0_0_0, 0))
        self.connect((self.blocks_int_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_int_to_float_0_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.blocks_int_to_float_0_0_0, 0), (self.blocks_magphase_to_complex_0, 0))
        self.connect((self.blocks_magphase_to_complex_0, 0), (self.blocks_null_sink_0_0, 2))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.traffic_gen_trigger_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_null_sink_0_0, 3))
        self.connect((self.traffic_gen_margin_cut_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.traffic_gen_mmse_resampler_cc_0, 0), (self.traffic_gen_margin_cut_0, 0))
        self.connect((self.traffic_gen_trigger_0, 0), (self.traffic_gen_mmse_resampler_cc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "modulated_traffic_gen")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tag_length(self):
        return self.tag_length

    def set_tag_length(self, tag_length):
        self.tag_length = tag_length

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_qam64(self):
        return self.qam64

    def set_qam64(self, qam64):
        self.qam64 = qam64

    def get_qam256(self):
        return self.qam256

    def set_qam256(self, qam256):
        self.qam256 = qam256

    def get_qam16(self):
        return self.qam16

    def set_qam16(self, qam16):
        self.qam16 = qam16

    def get_psk8(self):
        return self.psk8

    def set_psk8(self, psk8):
        self.psk8 = psk8

    def get_psk4(self):
        return self.psk4

    def set_psk4(self, psk4):
        self.psk4 = psk4

    def get_psk2(self):
        return self.psk2

    def set_psk2(self, psk2):
        self.psk2 = psk2

    def get_margin(self):
        return self.margin

    def set_margin(self, margin):
        self.margin = margin
        self.traffic_gen_trigger_0.set_margin(self.margin)

    def get_const_QAM16(self):
        return self.const_QAM16

    def set_const_QAM16(self, const_QAM16):
        self.const_QAM16 = const_QAM16



def main(top_block_cls=modulated_traffic_gen, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
