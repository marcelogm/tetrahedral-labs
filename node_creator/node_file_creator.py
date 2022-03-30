

class NodeEleFileCreator:

    def create_node(self, arr, output_name):
        file = open(output_name + ".node", "w+")
        file.write("# Node count, 3 dim, no attribute, no boundary marker\n")
        file.write("%d %d %d %d\n" %(len(arr), 3, 0, 0))
        file.write("# Node index, node coordinates\n")
        for i in range(len(arr)):
            file.write("%d %f %f %f\n" %(i, arr[i][0], arr[i][1], arr[i][2]))
        file.close()

    def create_ele(self, arr, output_name):
        file = open(output_name + ".ele", "w+")
        file.write("# Node count, 4 corners, no attribute\n")
        file.write("%d %d %d\n" %(len(arr), 4, 0))
        file.write("# Node index, corner indexes\n")
        for i in range(len(arr)):
            file.write("%d %d %d %d %d\n" %(i, arr[i][0], arr[i][1], arr[i][2], arr[i][3]))
        file.close()