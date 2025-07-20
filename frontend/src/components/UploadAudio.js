import React, { useState } from 'react';
import { API } from 'aws-amplify';
import axios from 'axios';

function UploadAudio() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadStatus('');
    }
  };

  const uploadFile = async () => {
    if (!file) return;
    
    setUploading(true);
    setProgress(0);
    setUploadStatus('Preparing upload...');
    
    try {
      // Step 1: Get a pre-signed URL from our API
      const apiName = 'echoguardApi';
      const path = '/upload-url';
      const data = {
        fileName: file.name,
        fileType: file.type
      };
      
      setUploadStatus('Getting upload URL...');
      const response = await API.post(apiName, path, { body: data });
      const { uploadURL, fileKey } = response;
      
      // Step 2: Upload directly to S3 using the pre-signed URL
      setUploadStatus('Uploading to S3...');
      await axios.put(uploadURL, file, {
        headers: {
          'Content-Type': file.type
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setProgress(percentCompleted);
        }
      });
      
      setUploadStatus('Upload complete! Processing will begin shortly.');
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus(`Error: ${error.message || 'Upload failed'}`);
    } finally {
      setTimeout(() => {
        setUploading(false);
        setFile(null);
        // Reset file input
        document.getElementById('file-upload').value = '';
      }, 3000);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Audio Recording</h2>
      <p className="upload-instructions">
        Upload an audio file to analyze for compliance issues.
        Supported formats: MP3, WAV, M4A
      </p>
      
      <input
        id="file-upload"
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
        disabled={uploading}
        className="file-input"
      />
      
      <button 
        className="upload-button"
        onClick={uploadFile} 
        disabled={!file || uploading}
      >
        {uploading ? 'Uploading...' : 'Upload Audio'}
      </button>
      
      {uploading && (
        <div className="upload-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="progress-text">{progress}%</div>
          <p className="status-text">{uploadStatus}</p>
        </div>
      )}
    </div>
  );
}

export default UploadAudio;