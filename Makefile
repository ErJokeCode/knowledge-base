first-start:
	python src/scripts.py --create-tables
	python src/scripts.py --create-bucket

pg-cr-tb:
	python src/scripts.py --create-tables

pg-dr-tb:
	python src/scripts.py --drop-tables

pg-recr-tb:
	python src/scripts.py --recreate-tables

minio-cr-bk:
	python src/scripts.py --create-bucket