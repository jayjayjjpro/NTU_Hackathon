import axios from 'axios';
import React, { useState } from 'react';
import './App.css';

const App = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileHash, setFileHash] = useState(null);

    const onFileChange = event => {
      const file = event.target.files[0];

      //Check for 50MB
      if (file.size > 50 * 1024 * 1024) { 
          alert("File size cannot exceed 50MB");
      } else {
          setSelectedFile(file);
      }
    };

    const onFileUpload = () => {
        const formData = new FormData();
        formData.append(
            "myFile",
            selectedFile,
            selectedFile.name
        );
        console.log(selectedFile);
        axios.post("https://server-upload-hsec.onrender.com/file/upload", formData)
        .then((response) => {
            console.log('Hash:', response.data);
            setFileHash(response.data);
        })
        .catch((error) => {
            console.error('Error uploading file:', error);
        });
    };

    const fileData = () => {
        if (selectedFile) {
            return (
                <div>
                    <h2>File Details:</h2>
                    <p>File Name: {selectedFile.name}</p>
                    <p>File Type: {selectedFile.type}</p>
                    <p>
                        Last Modified:{" "}
                        {selectedFile.lastModifiedDate.toDateString()}
                    </p>
                </div>
            );
        } else {
            return (
                <div>
                    <br />
                    <h4>Choose a File before Pressing the Upload button</h4>
                </div>
            );
        }
    };

    return (
        <div>
            <h1>Upload your file here</h1>
            <div>
                <input type="file" onChange={onFileChange} accept=".csv,.xlsx,.txt,.db" />
                <button onClick={onFileUpload}>Upload!</button>
            </div>
            {fileData()}
            {fileHash && (
            <div>
                <h2>File Hash:</h2>
                <p>{fileHash}</p>
            </div>
        )}
        </div>
    );
}

export default App;
