import os
from modules.utils import *
from modules.downloader import *
from modules.show import *
from modules.csv_downloader import *

from modules.utils import bcolors as bc

def image_level(args, DEFAULT_OID_DIR):

	if args.version == 'v4':
		"""
		'v4': 'https://storage.googleapis.com/openimages/2018_04/',
		"""
		if not args.dataset:
			dataset_dir = os.path.join(DEFAULT_OID_DIR, 'Dataset_nl')
			csv_dir = os.path.join(os.path.join(DEFAULT_OID_DIR, 'csv_folder_nl'), 'v4')
		else:
			dataset_dir = os.path.join(DEFAULT_OID_DIR, args.dataset)
			csv_dir = os.path.join(os.path.join(DEFAULT_OID_DIR, 'csv_folder_nl'), 'v4')

		name_file_class = 'class-descriptions.csv'
		CLASSES_CSV = os.path.join(csv_dir, name_file_class)

		if args.sub is None:
				print(bc.FAIL + 'Missing subset argument.' + bc.ENDC)
				exit(1)

		if args.sub == 'h':
			file_list = ['train-annotations-human-imagelabels.csv', \
						'validation-annotations-human-imagelabels.csv', \
						'test-annotations-human-imagelabels.csv']

		if args.sub == 'm':
			file_list = ['train-annotations-machine-imagelabels.csv', \
						'validation-annotations-machine-imagelabels.csv', \
						'test-annotations-machine-imagelabels.csv']

		if args.sub == 'h' or args.sub == 'm':
			logo(args.command)
			if args.type_csv is None:
				print(bc.FAIL + 'Missing type_csv argument.' + bc.ENDC)
				exit(1)
			if args.classes is None:
				print(bc.FAIL + 'Missing classes argument.' + bc.ENDC)
				exit(1)
			if args.multiclasses is None:
				args.multiclasses = 0

			folder = ['train', 'validation', 'test']

			if args.classes[0].endswith('.txt'):
				with open(args.classes[0]) as f:
					args.classes = f.readlines()
					args.classes = [x.strip() for x in args.classes]
			else:
					args.classes = [arg.replace('_', ' ') for arg in args.classes]

			if args.multiclasses == '0':

				mkdirs(args.version, dataset_dir, csv_dir, args.classes, args.type_csv)

				for classes in args.classes:
					class_name = classes

					error_csv(args.version, name_file_class, csv_dir, args.yes)
					df_classes = pd.read_csv(CLASSES_CSV, header=None)

					class_code = df_classes.loc[df_classes[1] == class_name].values[0][0]

					if args.type_csv == 'train':
						name_file = file_list[0]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[0], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[0], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'validation':
						name_file = file_list[1]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[1], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[1], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'test':
						name_file = file_list[2]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[2], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[2], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'all':
						for i in range(3):
							name_file = file_list[i]
							df_val = TTV(args.version,csv_dir, name_file, args.yes)
							if not args.n_threads:
								download(args, df_val, folder[i], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[i], dataset_dir, class_name, class_code, threads = int(args.n_threads))
					else:
						print(bc.FAIL + 'csv file not specified' + bc.ENDC)
						exit(1)

			elif args.multiclasses == '1':

				class_list = args.classes
				print(bc.INFO + "Downloading {} together.".format(class_list) + bc.ENDC)
				multiclass_name = ['_'.join(class_list)]
				mkdirs(args.version, dataset_dir, csv_dir, multiclass_name, args.type_csv)

				error_csv(args.version, name_file_class, csv_dir, args.yes)
				df_classes = pd.read_csv(CLASSES_CSV, header=None)

				class_dict = {}
				for class_name in class_list:
					class_dict[class_name] = df_classes.loc[df_classes[1] == class_name].values[0][0]

				for class_name in class_list:

					if args.type_csv == 'train':
						name_file = file_list[0]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[0], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[0], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'validation':
						name_file = file_list[1]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[1], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[1], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'test':
						name_file = file_list[2]
						df_val = TTV(args.version,csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[2], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[2], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'all':
						for i in range(3):
							name_file = file_list[i]
							df_val = TTV(args.version,csv_dir, name_file, args.yes)
							if not args.n_threads:
								download(args, df_val, folder[i], dataset_dir, class_name, class_dict[class_name], class_list)
							else:
								download(args, df_val, folder[i], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))
	
	elif args.version == 'v5':
		# TODO: Integration of OID v5 url links
		"""
		'v5': 'https://storage.googleapis.com/openimages/v5/',
		"""
		print("You had requested v5 of OpenImage Dataset.")

	elif args.version == 'v6':
		# TODO: Integration of OID v6 url links
		"""
        'v6': 'https://storage.googleapis.com/openimages/v5/'
		"""
		print("You had requested v6 of OpenImage Dataset.")

		if not args.dataset:
			dataset_dir = os.path.join(DEFAULT_OID_DIR, 'Dataset_nl')
			csv_dir = os.path.join(os.path.join(DEFAULT_OID_DIR, 'csv_folder_nl'), 'v6')
		else:
			dataset_dir = os.path.join(DEFAULT_OID_DIR, args.dataset)
			csv_dir = os.path.join(os.path.join(DEFAULT_OID_DIR, 'csv_folder_nl'), 'v6')

# https://storage.googleapis.com/openimages/v6/oidv6-class-descriptions.csv

		name_file_class = 'oidv6-class-descriptions.csv'
		CLASSES_CSV = os.path.join(csv_dir, name_file_class)

		if args.sub is None:
				print(bc.FAIL + 'Missing subset argument.' + bc.ENDC)
				exit(1)
# https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
# https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv
# https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv
# https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv	

		if args.sub == 'h':
			file_list = ['oidv6-train-annotations-human-imagelabels.csv', \
						'validation-annotations-human-imagelabels.csv', \
						'test-annotations-human-imagelabels.csv']

		if args.sub == 'm':
			file_list = ['train-annotations-machine-imagelabels.csv', \
						'validation-annotations-machine-imagelabels.csv', \
						'test-annotations-machine-imagelabels.csv']

		if args.sub == 'h' or args.sub == 'm':
			logo(args.command)
			if args.type_csv is None:
				print(bc.FAIL + 'Missing type_csv argument.' + bc.ENDC)
				exit(1)
			if args.classes is None:
				print(bc.FAIL + 'Missing classes argument.' + bc.ENDC)
				exit(1)
			if args.multiclasses is None:
				args.multiclasses = 0

			folder = ['train', 'validation', 'test']

			if args.classes[0].endswith('.txt'):
				with open(args.classes[0]) as f:
					args.classes = f.readlines()
					args.classes = [x.strip() for x in args.classes]
			else:
					args.classes = [arg.replace('_', ' ') for arg in args.classes]

			if args.multiclasses == '0':

				mkdirs(args.version, dataset_dir, csv_dir, args.classes, args.type_csv)

				for classes in args.classes:
					class_name = classes

					error_csv(args.version, name_file_class, csv_dir, args.yes)
					df_classes = pd.read_csv(CLASSES_CSV, header=None)

					class_code = df_classes.loc[df_classes[1] == class_name].values[0][0]

					if args.type_csv == 'train':
						name_file = file_list[0]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[0], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[0], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'validation':
						name_file = file_list[1]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[1], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[1], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'test':
						name_file = file_list[2]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[2], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[2], dataset_dir, class_name, class_code, threads = int(args.n_threads))

					elif args.type_csv == 'all':
						for i in range(3):
							name_file = file_list[i]
							df_val = TTV(args.version, csv_dir, name_file, args.yes)
							if not args.n_threads:
								download(args, df_val, folder[i], dataset_dir, class_name, class_code)
						else:
							download(args, df_val, folder[i], dataset_dir, class_name, class_code, threads = int(args.n_threads))
					else:
						print(bc.FAIL + 'csv file not specified' + bc.ENDC)
						exit(1)

			elif args.multiclasses == '1':

				class_list = args.classes
				print(bc.INFO + "Downloading {} together.".format(class_list) + bc.ENDC)
				multiclass_name = ['_'.join(class_list)]
				mkdirs(args.version, dataset_dir, csv_dir, multiclass_name, args.type_csv)

				error_csv(args.version, name_file_class, csv_dir, args.yes)
				df_classes = pd.read_csv(CLASSES_CSV, header=None)

				class_dict = {}
				for class_name in class_list:
					class_dict[class_name] = df_classes.loc[df_classes[1] == class_name].values[0][0]

				for class_name in class_list:

					if args.type_csv == 'train':
						name_file = file_list[0]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[0], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[0], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'validation':
						name_file = file_list[1]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[1], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[1], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'test':
						name_file = file_list[2]
						df_val = TTV(args.version, csv_dir, name_file, args.yes)
						if not args.n_threads:
							download(args, df_val, folder[2], dataset_dir, class_name, class_dict[class_name], class_list)
						else:
							download(args, df_val, folder[2], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))

					elif args.type_csv == 'all':
						for i in range(3):
							name_file = file_list[i]
							df_val = TTV(args.version, csv_dir, name_file, args.yes)
							if not args.n_threads:
								download(args, df_val, folder[i], dataset_dir, class_name, class_dict[class_name], class_list)
							else:
								download(args, df_val, folder[i], dataset_dir, class_name, class_dict[class_name], class_list, int(args.n_threads))
