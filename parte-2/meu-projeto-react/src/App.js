import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [processList, setProcessList] = useState([]);
  const [image, setImage] = useState('');
  const [newProcess, setNewProcess] = useState({
    tempo_chegada: '',
    tempo_execucao: '',
    deadline: '',
    quantum_sistema: '',
    sobrecarga_sistema: ''
   
  });
  const [selectedScheduler, setSelectedScheduler] = useState(1); // 1 for FIFO, 2 for Round Robin, 3 for EDF, 4 for SJF

  useEffect(() => {
    axios.get('http://localhost:8000/getprocesslist')
      .then(response => {
        setProcessList(response.data.process);
      })
      .catch(error => {
        console.error('Error fetching process list:', error);
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewProcess({
      ...newProcess,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const processData = {
      ...newProcess,
       
    };

    axios.post('http://localhost:8000/newprocess', processData)
      .then(response => {
        setProcessList(response.data.process);
        setNewProcess({
          tempo_chegada: '',
          tempo_execucao: '',
          deadline: '',
          quantum_sistema: '',
          sobrecarga_sistema: '',
          
        });
      })
      .catch(error => {
        console.error('There was an error adding the process!', error);
      });
  };

  const createGraph = () => {
    axios.post('http://localhost:8000/creategraph', { tipo_escalonador: selectedScheduler })
      .then(response => {
        setImage(`data:text/html;base64,${btoa(response.data.html)}`);
      })
      .catch(error => {
        console.error('There was an error creating the graph!', error);
      });
  };

  return (
    <div className="App">
      <h1>Process Scheduler</h1>

      <form onSubmit={handleSubmit}>
        <h2>Add New Process</h2>
        <div>
          <label>Tempo Chegada:
            <input
              type="number"
              name="tempo_chegada"
              value={newProcess.tempo_chegada}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        <div>
          <label>Tempo Execução:
            <input
              type="number"
              name="tempo_execucao"
              value={newProcess.tempo_execucao}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        <div>
          <label>Deadline:
            <input
              type="number"
              name="deadline"
              value={newProcess.deadline}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        
            <div>
              <label>Quantum Sistema:
                <input
                  type="number"
                  name="quantum_sistema"
                  value={newProcess.quantum_sistema}
                  onChange={handleChange}
                  required
                />
              </label>
            </div>
            <div>
              <label>Sobrecarga Sistema:
                <input
                  type="number"
                  name="sobrecarga_sistema"
                  value={newProcess.sobrecarga_sistema}
                  onChange={handleChange}
                  required
                />
              </label>
            </div>
       
        <button type="submit">Add Process</button>
      </form>
      <div>
        <h2>Select Scheduler</h2>
        <button onClick={() => setSelectedScheduler(1)}>FIFO</button>
        <button onClick={() => setSelectedScheduler(3)}>Round Robin</button>
        <button onClick={() => setSelectedScheduler(4)}>EDF</button>
        <button onClick={() => setSelectedScheduler(2)}>SJF</button>
      </div>

      <button onClick={createGraph}>Create Graph</button>
      {image && <iframe src={image} width="1200" height="800" title="Process Graph" />}

      <div>
        <h2>Process List</h2>
        <ul>
          {processList.map((process) => (
            <li key={process.id}>
              ID: {process.id}, Tempo Chegada: {process.tempo_chegada}, Tempo Execução: {process.tempo_execucao}, Deadline: {process.deadline}, Sobrecarga: {process.sobrecarga_sistema}, Quantum: {process.quantum_sistema}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
export default App;
