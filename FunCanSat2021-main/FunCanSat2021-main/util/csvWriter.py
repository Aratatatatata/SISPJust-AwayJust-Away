import csv

class csvWriter:
    def __init__(self, dirPath, fileName):
        self.path = dirPath+fileName
        if not(os.path.isdir(dirPath)):
            os.makedirs(dirPath)
        f = open(self.path, 'w')
        f.close()
    
    def write(self, data):
        with open(self.path, 'w') as f:
            writer = csv.writer(f,lineterminator='\n')
            writer.writerow(data)


