class ArgumentParser:
    def __init__(self):
        self.source_folder = None
        self.output_folder = None
        self.user_input(self)

    def user_input(self, args):
        self.source_folder = input("Enter source folder: ").strip()
        self.output_folder = input("Enter output folder: ").strip()
