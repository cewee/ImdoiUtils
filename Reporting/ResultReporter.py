### Reporting tool to describe results generated in a docker container(online platform imdroi.com)
import json
class OutputElement(object):
    def __init__(self, output_id, tag):
        self.element = {}
        self.element["output_id"] = output_id
        self.element["tag"] = tag
        self.element["type"] = "##"
        self.element["subtype"] = "##"
        self.element["representation"] = {}

    def setEllipse(self,x1,y1,x2,y2,slices, color=None):
        self.element["type"] = "roi"
        self.element["subtype"] = "ellipse"
        self.element["representation"]["tlhc"] = [x1,y1]
        self.element["representation"]["brhc"] = [x2,y2]
        self.element["representation"]["slices"] = slices
        self.element["representation"]["color"] = color

    def setAttachment(self,filePath, fileType):
        self.element["type"] = "attachment"
        self.element["subtype"]= fileType
        self.element["representation"]["file_path"] = filePath
    def setDiagnosisText(self, text):
        self.element["type"] = "text"
        self.element["subtype"]= "diagnosis"
        self.element["representation"]["diagnosis_text"] = text

    def getElement(self,):
        return self.element


class ResultReporter(object):
    def __init__(self, app_id, app_name):
        self.report = {}
        self.report["app_id"] = app_id
        self.report["app_name"] = app_name
        self.report["elements"] = []

    def addElement(self, output):
        self.report["elements"].append(output.getElement())

    def getJSON(self):
        return json.dumps(self.report, indent=2)
