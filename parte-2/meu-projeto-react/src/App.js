import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logoUFBA from '../src/images/svg-ufba.svg';
import logoIC from '../src/images/svg-ic.svg';
import '../src/App.css'; // Importe o CSS

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
  const [submitted, setSubmitted] = useState(false); // Definindo o estado submitted

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
  const clearProcessList = () => {
    axios.post('http://localhost:8000/clear') // Ajuste a URL conforme necessário
      .then(response => {
        setProcessList([]); // Limpa a lista de processos no frontend
      })
      .catch(error => {
        console.error('There was an error clearing the process list!', error);
      });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const processData = {
		tempo_chegada: newProcess.tempo_chegada,
		tempo_execucao: newProcess.tempo_execucao,
		deadline: newProcess.deadline,
		quantum_sistema: newProcess.quantum_sistema, // Manter os valores de quantum e sobrecarga
		sobrecarga_sistema: newProcess.sobrecarga_sistema // Manter os valores de quantum e sobrecarga
	  };

	  axios.post('http://localhost:8000/newprocess', processData)
      .then(response => {
        setProcessList(response.data.process);
        setNewProcess((prevState) => ({
          ...prevState,
          tempo_chegada: '',
          tempo_execucao: '',
          deadline: ''
        }));
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
      <div className='header'>
        <img src={logoUFBA} />
        <div className='navbar'>
          <h1>Escalonador de Processos</h1>

          <form onSubmit={handleSubmit}>
            <div className='input-global'>

              <div className='quantum-sobrecarga'>

                <div className='label'>
                  <label htmlfor="quantum" className='inputName'>Quantum</label>

                  <input type="number" id="quantum" name="quantum_sistema" value={newProcess.quantum_sistema}
                    onChange={handleChange}

                  />

                </div>
                <div className='label'>
                  <label for="sobrecarga" className='inputName'>Sobrecarga</label>
                  <input type="number" id="sobrecarga" name="sobrecarga_sistema" value={newProcess.sobrecarga_sistema}
                    onChange={handleChange}
                  />
                </div>
              </div>
              <div className='container'>
                <div className='radio-tile-group'>

                  <button
                    className={`scheduler-button ${selectedScheduler === 'FIFO' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('FIFO')}
                  >
                    FIFO
                  </button>

                  <button
                    className={`scheduler-button ${selectedScheduler === 'SJF' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('SJF')}
                  >
                    SJF
                  </button>

                  <button
                    className={`scheduler-button ${selectedScheduler === 'RR' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('RR')}
                  >
                    Round Robin
                  </button>

                  <button
                    className={`scheduler-button ${selectedScheduler === 'EDF' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('EDF')}
                  >
                    EDF
                  </button>
                </div>
              </div>

            </div>
          </form>

        </div>
        <img src={logoIC} />

      </div>


      <div></div>
      <form onSubmit={handleSubmit}>
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




        <div className='form-buttons'>
          <button type="submit">Adicionar processo</button>
          <button type="button" onClick={clearProcessList}>Limpar lista de processos</button>
        </div>

      </form>

      <button onClick={createGraph}>Criar Gráfico</button>
      {image && <iframe src={image} width="1200" height="800" title="Process Graph" />}

      <div>
        <h2>Lista de processos</h2>
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
