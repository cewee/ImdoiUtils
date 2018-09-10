import ResultReporter

d = ResultReporter.ResultReporter("TestApp_ID", "TestApp")
output1 = ResultReporter.OutputElement("id1", "tag1")
# Create ellipse element which at with bounding box top left (1,1) and bottom right (50,50), which is visible on slices 0 and 2
# color of ellipse is orange
output1.setEllipse(1,1,50,50,[0,2],"orange")

# Create PDF attachment
output2 = ResultReporter.OutputElement("id2", "tag2")
output2.setAttachment("/tmp/result.pdf", "pdf")

# Add elements to result report
d.addElement(output1)
d.addElement(output2)
# Print json desciption of produced results
print (d.getJSON())
