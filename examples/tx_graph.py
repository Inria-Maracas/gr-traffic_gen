#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Transmitter
# Author: cyrille
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
from gnuradio.qtgui import Range, RangeWidget
import traffic_gen
from gnuradio import qtgui

class tx_graph(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transmitter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transmitter")
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

        self.settings = Qt.QSettings("GNU Radio", "tx_graph")

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
        self.total_sample = total_sample = 2000000
        self.tagname = tagname = "start_pack"
        self.samp_rate = samp_rate = 10000
        self.qam64 = qam64 = digital.qam.qam_constellation(constellation_points=64, differential=True, mod_code='none', large_ampls_to_corners=False)
        self.qam256 = qam256 = digital.qam.qam_constellation(constellation_points=256, differential=True, mod_code='none', large_ampls_to_corners=False)
        self.margin = margin = 250
        self.filename = filename = "exemple_1"
        self.const_QAM16 = const_QAM16 = digital.constellation_16qam().base()

        ##################################################
        # Blocks
        ##################################################
        self._margin_range = Range(0, 1000, 1, 250, 200)
        self._margin_win = RangeWidget(self._margin_range, self.set_margin, 'Margin', "counter_slider", float)
        self.top_grid_layout.addWidget(self._margin_win)
        self.traffic_gen_trigger_0_0_0 = traffic_gen.trigger('127.0.0.1', 7000, tagname, margin, 'qam256', 2, samp_rate)
        self.traffic_gen_trigger_0_0 = traffic_gen.trigger('127.0.0.1', 7000, tagname, margin, 'qam64', 1, samp_rate)
        self.traffic_gen_trigger_0 = traffic_gen.trigger('127.0.0.1', 7000, tagname, margin, 'qam16', 0, samp_rate)
        self.traffic_gen_mmse_resampler_cc_0_0_0 = traffic_gen.mmse_resampler_cc(0, 1, tagname)
        self.traffic_gen_mmse_resampler_cc_0_0 = traffic_gen.mmse_resampler_cc(0, 1, tagname)
        self.traffic_gen_mmse_resampler_cc_0 = traffic_gen.mmse_resampler_cc(0, 1, tagname)
        self.traffic_gen_margincut_0_0_0 = traffic_gen.margincut(margin, margin, tagname, True)
        self.traffic_gen_margincut_0_0 = traffic_gen.margincut(margin, margin, tagname, True)
        self.traffic_gen_margincut_0 = traffic_gen.margincut(margin, margin, tagname, True)
        self.traffic_gen_labelisator_1 = traffic_gen.labelisator(filename, tagname, margin, total_sample)
        self.traffic_gen_insert_burst_0_0_0 = traffic_gen.insert_burst( tagname, margin, True)
        self.traffic_gen_insert_burst_0_0 = traffic_gen.insert_burst( tagname, margin, True)
        self.traffic_gen_insert_burst_0 = traffic_gen.insert_burst( tagname, margin, True)
        self.traffic_gen_gate_0 = traffic_gen.gate(total_sample)
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.digital_chunks_to_symbols_xx_0_0_0_0 = digital.chunks_to_symbols_bc(qam256.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(qam64.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(const_QAM16.points(), 1)
        self.blocks_throttle_1_0_1_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_1_0_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_1_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tag_debug_1 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'end', "")
        self.blocks_tag_debug_1.set_display(True)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, 'output', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)
        self.analog_random_source_x_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2**4, 100000))), True)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2**4, 100000))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2**4, 100000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_UNIFORM, 0.01, 0)
        self.analog_const_source_x_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.traffic_gen_trigger_0, 'freq'), (self.analog_sig_source_x_0_0, 'freq'))
        self.msg_connect((self.traffic_gen_trigger_0_0, 'freq'), (self.analog_sig_source_x_0, 'freq'))
        self.msg_connect((self.traffic_gen_trigger_0_0_0, 'freq'), (self.analog_sig_source_x_0_1, 'freq'))
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.analog_random_source_x_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.traffic_gen_gate_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_1_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_throttle_1_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_throttle_1_0_1_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.traffic_gen_insert_burst_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.traffic_gen_insert_burst_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.traffic_gen_insert_burst_0_0_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_throttle_1_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle_1_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_throttle_1_0_1_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.traffic_gen_trigger_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.traffic_gen_trigger_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0_0, 0), (self.traffic_gen_trigger_0_0_0, 0))
        self.connect((self.traffic_gen_gate_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.traffic_gen_gate_0, 0), (self.blocks_tag_debug_1, 0))
        self.connect((self.traffic_gen_gate_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.traffic_gen_gate_0, 0), (self.traffic_gen_labelisator_1, 0))
        self.connect((self.traffic_gen_insert_burst_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.traffic_gen_insert_burst_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.traffic_gen_insert_burst_0_0_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.traffic_gen_margincut_0, 0), (self.traffic_gen_insert_burst_0, 1))
        self.connect((self.traffic_gen_margincut_0_0, 0), (self.traffic_gen_insert_burst_0_0, 1))
        self.connect((self.traffic_gen_margincut_0_0_0, 0), (self.traffic_gen_insert_burst_0_0_0, 1))
        self.connect((self.traffic_gen_mmse_resampler_cc_0, 0), (self.traffic_gen_margincut_0, 0))
        self.connect((self.traffic_gen_mmse_resampler_cc_0_0, 0), (self.traffic_gen_margincut_0_0, 0))
        self.connect((self.traffic_gen_mmse_resampler_cc_0_0_0, 0), (self.traffic_gen_margincut_0_0_0, 0))
        self.connect((self.traffic_gen_trigger_0, 0), (self.traffic_gen_mmse_resampler_cc_0, 0))
        self.connect((self.traffic_gen_trigger_0_0, 0), (self.traffic_gen_mmse_resampler_cc_0_0, 0))
        self.connect((self.traffic_gen_trigger_0_0_0, 0), (self.traffic_gen_mmse_resampler_cc_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_graph")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_total_sample(self):
        return self.total_sample

    def set_total_sample(self, total_sample):
        self.total_sample = total_sample

    def get_tagname(self):
        return self.tagname

    def set_tagname(self, tagname):
        self.tagname = tagname

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_1_0_1_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_qam64(self):
        return self.qam64

    def set_qam64(self, qam64):
        self.qam64 = qam64

    def get_qam256(self):
        return self.qam256

    def set_qam256(self, qam256):
        self.qam256 = qam256

    def get_margin(self):
        return self.margin

    def set_margin(self, margin):
        self.margin = margin
        self.traffic_gen_trigger_0.set_margin(self.margin)
        self.traffic_gen_trigger_0_0.set_margin(self.margin)
        self.traffic_gen_trigger_0_0_0.set_margin(self.margin)

    def get_filename(self):
        return self.filename

    def set_filename(self, filename):
        self.filename = filename

    def get_const_QAM16(self):
        return self.const_QAM16

    def set_const_QAM16(self, const_QAM16):
        self.const_QAM16 = const_QAM16



def main(top_block_cls=tx_graph, options=None):

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
