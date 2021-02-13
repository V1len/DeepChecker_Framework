import utils

if __name__ == '__main__':
    directory_path = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/old_directory_3D.json"
    new_directory_path = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/old_directory.json"
    latex_format_path = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/latex_format.txt"
    directory = utils.ReadJson(directory_path)
    new_directory = []
    latex_format = ""
    for index in range(len(directory)):
        item = directory[index]
        reverse_item = item[::-1]
        new_directory.append(reverse_item)
        lettermark = False
        firstmark = True
        for i in range(len(reverse_item)):
            if reverse_item[i] != "-":
                if lettermark == False:
                    lettermark = True
                    if firstmark == False:
                        latex_format += "|"
                    else:
                        firstmark = False
                    latex_format += "\\mathtt{"
                latex_format += reverse_item[i]
            else:
                if lettermark == True:
                    lettermark = False
                    latex_format += "}\\verb|"
                latex_format += "-"
        if lettermark == True:
            latex_format += "}"
        else:
            latex_format += "|"
        if index != len(directory) - 1:
            latex_format += ", "

    utils.WriteJson(new_directory, new_directory_path)
    print(latex_format)
    utils.WriteJson(latex_format, latex_format_path)


    