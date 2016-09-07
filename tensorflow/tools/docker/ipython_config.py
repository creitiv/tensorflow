c = get_config()

# Add a path to our search path to be able to import modules installed outside of the container
c.InteractiveShellApp.exec_lines = ['import sys; sys.path.append("/data/packages/lib/python")']
