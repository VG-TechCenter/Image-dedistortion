clc;
clear;
close all;

images = imageSet(fullfile('C:\Users\Kylin\Desktop\VG-Tech\相机标定加去畸变\imgset'));

imageFileNames = images.ImageLocation;

[imagePoints, boardSize] = detectCheckerboardPoints(imageFileNames);

squareSizeInMM = 9;
worldPoints = generateCheckerboardPoints(boardSize,squareSizeInMM);

I = readimage(images,1); 
imageSize = [size(I, 1),size(I, 2)];
params = estimateCameraParameters(imagePoints,worldPoints, ...
                                  'ImageSize',imageSize);

showReprojectionErrors(params);


figure;
showExtrinsics(params);
drawnow;

figure; 
imshow(imageFileNames{1}); 
hold on;
plot(imagePoints(:,1,1), imagePoints(:,2,1),'go');
plot(params.ReprojectedPoints(:,1,1),params.ReprojectedPoints(:,2,1),'r+');
legend('Detected Points','ReprojectedPoints');
hold off;


I = images.readimage(1);
J1 = undistortImage(I,params);

figure; imshowpair(I,J1,'montage');
title('Original Image (left) vs. Corrected Image (right)');

J2 = undistortImage(I,params,'OutputView','full');
figure; 
imshow(J2);
title('Full Output View');
