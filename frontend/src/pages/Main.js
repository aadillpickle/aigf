import React, { useState, useEffect, useRef } from "react";
import LoadingSpinner from "../LoadingSpinner";
import VoiceRecorderButton from "./VoiceRecorderButton";
import defaultImg from "../ahrii.png";

function Main() {
  const inputRef = useRef(null);
  const videoRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState("");

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.load();
    }
  }, [videoUrl]);

  const handleTranscription = (transcript) => {
    inputRef.current.value += transcript;
    inputRef.current.selectionStart = inputRef.current.selectionEnd =
      inputRef.current.value.length;
    inputRef.current.scrollLeft = inputRef.current.scrollWidth;
    inputRef.current.scrollTop = inputRef.current.scrollHeight;
  };


  const handleSubmit = async (event) => {
    setLoading(true);
    const input = inputRef.current.value;
    inputRef.current.value = "";
    event.preventDefault();
    const requestParams = {input};
    console.log(process.env.REACT_APP_API_ROOT)
    const resp = await fetch(process.env.REACT_APP_API_ROOT + "/get-video-from-chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestParams),
    });

    if (resp.ok) {
      const response = await resp.json();
      const video_url = response["video_url"];
      setVideoUrl(video_url);
    } else {
      console.error("Failed to fetch video:", resp.status, resp.statusText);
    }
    
    setLoading(false);
  };
  
  return (
    <div className="bg-transparent w-full h-screen flex flex-col items-center mb-4 justify-center gap-4">
      <div className="text-lg w-5/6 md:text-4xl md:w-1/3 text-center font-sans text-slate-700 mb-4 font-bold">
        Ai Anime GF
      </div>
      <textarea
        id="message"
        rows="4"
        ref={inputRef}
        maxLength={625}
        class="block p-2.5 w-3/4 md:w-1/3 text-base text-slate-600 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
        placeholder="love me senpai"
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            handleSubmit(event);
          }
        }}
      ></textarea>
      <VoiceRecorderButton
        onTranscribe={handleTranscription}
      />
      <button
        className={
          "rounded-md text-lg w-3/4 md:w-1/3 h-16 text-white bg-slate-800 disabled:opacity-50"
        }
        onClick={handleSubmit}
        disabled={loading}
      >
        Submit
      </button>
      {loading && (<LoadingSpinner/>)}

      {videoUrl && <video ref={videoRef} autoPlay className="w-3/4 md:w-1/3">
        <source src={videoUrl} type="video/mp4" />
      </video>}

      {!videoUrl && <img src={defaultImg} alt="default" className="w-3/4 md:w-1/3"/>}
    </div>
  );
}

export default Main;
