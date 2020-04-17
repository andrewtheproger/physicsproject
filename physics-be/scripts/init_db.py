import os
from pathlib import Path

root = Path(os.path.dirname(os.path.realpath(__file__)))


def rmdir_force(path) :
    for sub in path.iterdir() :
        if sub.is_dir() :
            rmdir_force(sub)
        else :
            sub.unlink()

    path.rmdir() 


def exec_crossplatform(command):
	if os.name == 'nt':
	    os.system(f'cmd /c {command}')
	elif os.name == 'posix':
	    os.system(cmd)
	else:
		raise Exception('Cant determinate os')


def find_git_root():
	current_dir = root
	while current_dir.parent != current_dir:
		for item in current_dir.iterdir():
			if item.name == '.git':
				return current_dir

		current_dir = current_dir.parent

	raise Exception(f'Cant find a git repository parent from {root}')


def main():
	git_root = find_git_root()
	print(f'Found a git repository at {git_root}')

	migrations = git_root/'physics-be'/'migrations'
	database = git_root/'physics-be'/'server'/'server.db'

	if migrations.is_dir():
		rmdir_force(migrations)
		print(f'Removed {migrations}')
	else:
		print('Migrations were not found, it is probably ok')
	
	if database.is_file():
		database.unlink()
		print(f'Removed {database}')
	else:
		print('Database was not found, it is probably ok')

	os.environ['FLASK_APP'] = str(git_root/'physics-be'/'server'/'server.py')

	print(os.getcwd())
	os.chdir(git_root/'physics-be')
	print(os.getcwd())

	print('=== init')
	exec_crossplatform('flask db init')
	print('=== migrate')
	exec_crossplatform('flask db migrate')
	print('=== upgrade')
	exec_crossplatform('flask db upgrade')

	print()
	print()
	print('ok')


if __name__ == '__main__':
    print(f'from root {root}')
    main()