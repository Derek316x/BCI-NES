# BCI-NES

Team Name: Bae-ta Waves

Team Members: 

Derek Netto, Columbia University 


Uma Mohan, Columbia University 


Ankeet Parikh, Rutgers University 


Salman Qasim, Columbia University 

Project: BCI-NES 

The goal of this project was to utilize a full suite of bio-potential and physical sensors through the OpenBCI framework to play console videogames on a computer. The novel aspect of this work is the ability of the user to play just about any console game available on emulators, with very little training using our hybrid-BCI. The logic of this attempt emerged from the idea that computer based console emulators must, by necessity, map the complicated and diverse controllers used by Microsoft, Sony, Nintendo, etc to a constant set of key presses on a standard computer keyboard. We could leverage this mapping by decoding brain/body activity and encoding it to the same key presses, giving users the ability to control not a single game but a vast library of them. 

In order to do this, our user would need several degrees of freedom. We planned to provide this through detection of: 
- eyeblinks: eyeblinks were detected via frontal EEG electrodes, and mapped to the "action button" (i.e. 'A' on an NES controller) 
- left and right muscle contraction: these were detected through forearm EMG electrodes, and mapped to left and right movement
- brief, lateral head movements: these were detected through the accelerometer, and mapped to the up and down movement
- detection of alpha power (8-13 Hz) increases: these were detected on any EEG electrode (starting with frontal), and mapped to the "Start" button  

The main difficulty we encountered was wrt to online streaming/processing/analysis of the raw OpenBCI data. Once we accomplished this, the next big roadblock was to set intelligent thresholding to allow for detection of the above events. We did not accoomplish this sufficiently in the time provided, but the idea was for every user to rest with their eyes open for 30 seconds prior to the task, allowing us to establish baseline values for all of the above signals and assess the quality of the signals. Then, during the task adaptive thresholds would respond to deviations in amplitude (or mean power, in the case of alphas) greater than 3*SD of a weighted average of the baseline signal and the previous window of incoming, online data.

We plan to extend this framework in the near future and hope to add videos to this Github (eventually) showing a fully functional BCI-NES experience! 

We'd like to give a big thanks to Dr. Iyad Obeid and Temple University for hosting us, and Dr. Paul Sajda for sponsoring our team.
