from stytra import TailTrackingExperiment
from stytra.stimulation.stimuli import ClosedLoop1D
from stytra.stimulation.backgrounds import gratings
from stytra.stimulation.closed_loop import VigourMotionEstimator
from PyQt5.QtWidgets import QSplitter, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt
from stytra.stimulation import Protocol

import multiprocessing


class ClosedLoopExperiment(TailTrackingExperiment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_layout = QSplitter(Qt.Horizontal)
        self.behaviour_layout = QSplitter(Qt.Vertical)
        self.behaviour_layout.addWidget(self.camera_viewer)
        self.behaviour_layout.addWidget(self.stream_plot)
        self.main_layout.addWidget(self.behaviour_layout)
        self.main_layout.addWidget(self.widget_control)
        self.setCentralWidget(self.main_layout)

        self.set_protocol(Protocol([
            ClosedLoop1D(background=gratings(mm_px=0.22, spatial_period=10),
                         fish_motion_estimator=VigourMotionEstimator(
                            self.data_acc_tailpoints), duration=100, default_velocity=10)
                        ]))
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    multiprocessing.set_start_method('spawn')
    exp = ClosedLoopExperiment(app=app, name='closed_loop',
                              directory=r'/Users/vilimstich/Temp',
                              tracking_method='angle_sweep',
                              video_input='/Users/vilimstich/PhD/Experimental/tail_movement.avi',
                              tracking_method_parameters={'num_points': 9,
                                                          'filtering': True,
                                                          'color_invert': False})
    app.exec_()
