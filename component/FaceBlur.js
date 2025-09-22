import { useEffect, useRef } from 'react';

const FaceBlur = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const startVideo = async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    };

    startVideo();

    return () => {
      const stream = videoRef.current.srcObject;
      const tracks = stream.getTracks();

      tracks.forEach(track => track.stop());
    };
  }, []);

  return (
    <video ref={videoRef} autoPlay playsInline width="640" height="480" />
  );
};

export default FaceBlur;
