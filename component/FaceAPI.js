import { useEffect, useRef } from 'react';
import * as faceapi from 'face-api.js';

const FaceBlur = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    const loadModels = async () => {
      await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
      await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
      await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
    };

    loadModels();

    const startVideo = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    };

    startVideo();

    videoRef.current.addEventListener('play', () => {
      const canvas = faceapi.createCanvasFromMedia(videoRef.current);
      canvasRef.current.append(canvas);
      const displaySize = { width: videoRef.current.width, height: videoRef.current.height };
      faceapi.matchDimensions(canvas, displaySize);

      setInterval(async () => {
        const detections = await faceapi.detectAllFaces(videoRef.current).withFaceLandmarks().withFaceDescriptors();
        canvas?.clear();
        faceapi.draw.drawDetections(canvas, detections);
        faceapi.draw.drawFaceLandmarks(canvas, detections);
        faceapi.draw.drawFaceExpressions(canvas, detections);
      }, 100);
    });

    return () => {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach(track => track.stop());
    };
  }, []);

  return (
    <div>
      <video ref={videoRef} autoPlay playsInline width="640" height="480" />
      <div ref={canvasRef} />
    </div>
  );
};

export default FaceBlur;
