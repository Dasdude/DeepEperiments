from plotContainer import PlotContainer
from visualizer_container import VisualizerContainer
from keras.utils.visualize_util import plot
import pickle
import os
class HistoryHolder():
	#CONSTANTS
	FOLDER_NAME_RESULTS="Results"
	FOLDER_NAME_FIGURES="Figures"
	FOLDER_NAME_PLOTS="Plots"
	RELATIVE_PATH_DEFAULT = "."
	#END_OF_CONSTANTS
	#FIELDS:
	# dir_abs_path='' # After init is /FOLDER_NAME_RESULTS/
	# plots_abs_path=''
	# figure_abs_path = ''
	# metric_plot_container=None
	# weight_visualizer_container = None
	# experiment_name = "TEST"
	# experiment_index = '0'
	#END_OF_FIELDS
	def __init__(self,experiment_name,opts,relative_result_path=RELATIVE_PATH_DEFAULT):
		self.experiment_name = experiment_name
		self.relative_result_path = os.path.join(relative_result_path, self.FOLDER_NAME_RESULTS, experiment_name)
		self.folder_creation_wrapper()
		self.metric_plot_container=PlotContainer(self.plots_abs_path, self.experiment_index)
		self.weight_visualizer_container =VisualizerContainer(self.figure_abs_path, self.experiment_index)
		self.opts=opts
	def folder_creation_wrapper(self):
		self.dir_abs_path = os.path.abspath(self.relative_result_path)
		self.create_main_folder_hierachy(self.relative_result_path)
		self.create_expriment_index()
		self.plots_abs_path = os.path.join(self.dir_abs_path,self.FOLDER_NAME_PLOTS)
		self.figure_abs_path = os.path.join(self.dir_abs_path, self.FOLDER_NAME_FIGURES)
		os.mkdir(self.plots_abs_path)
		os.mkdir(self.figure_abs_path)
	def create_expriment_index(self):
		i=1
		abs_path = self.dir_abs_path
		while True:
			if os.path.exists(os.path.join(abs_path,str(i))):
				i=i+1
			else:
				os.mkdir(os.path.join(abs_path,str(i)))
				self.experiment_index=str(i)
				break
		self.dir_abs_path = os.path.join(abs_path,self.experiment_index)


	def create_main_folder_hierachy(self,relative_result_path):
		abs_path = os.path.abspath(relative_result_path)
		self.createFolderPath(abs_path)

	def createFolderPath(self,abs_path):
		# making sure all the folders in the path exist o.w. creating those folders
		folder_list = abs_path.split('/')
		path_to_be_created = ''
		for folder in folder_list[1:]:
			path_to_be_created += '/' + folder
			if not os.path.exists(path_to_be_created):
				os.mkdir(path_to_be_created)
	def model_plot(self,model):
		plot(model, to_file=self.dir_abs_path+'/model.png')
	def store_opts(self):
		with open(self.dir_abs_path+'/opts.pkl', 'wb') as f:
			pickle.dump(self.opts, f, 0)
	## TODO: create a funciton to store the state in the results folder at the time its called
if __name__ == '__main__':
    hh = HistoryHolder(experiment_name="test_hh")
    hh.metric_plot_container.create_random_plots()
    print hh.relative_result_path
