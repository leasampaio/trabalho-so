import React, { useState, useEffect } from 'react';
import axios from 'axios';
import logoUFBA from '../src/images/svg-ufba.svg';
import logoIC from '../src/images/svg-ic.svg';
import '../src/App.css'; // Importe o CSS

function App() {
  const [processList, setProcessList] = useState([]);
  const [turnaroundList, setTurnaroundList] = useState([]);
  const [loading, setLoading] = useState(false); // Estado para indicar carregamento
  const [error, setError] = useState(null); //
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


  const [showTurnaroundBox, setShowTurnaroundBox] = useState(false);


  const fetchTurnaroundList = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/getturnaroundlist');

      // Verifica se a resposta contém o array e se é um array
      if (Array.isArray(response.data)) {
        const turnaroundNames = ['FIFO', 'SJF', 'RR', 'EDF'];
        const turnaroundData = response.data.map((value, index) => ({
          name: turnaroundNames[index],
          value: value.toFixed(2) // Formata o valor com duas casas decimais
        }));
        setTurnaroundList(turnaroundData);
        setShowTurnaroundBox(true); // Exibe a caixinha com os turnarounds
      } else {
        throw new Error('Formato de dados inesperado');
      }
    } catch (error) {
      setError('Erro ao buscar a lista de turnarounds.');
      console.error('Erro ao buscar a lista de turnarounds:', error);
    } finally {
      setLoading(false);
    }
  };


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
        // Limpa a lista de processos no frontend
        setTurnaroundList([]); // Limpa a lista de turnarounds
        setShowTurnaroundBox(false);
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
                    type="button"
                    className={`scheduler-button ${selectedScheduler === 'FIFO' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('FIFO')}
                  >
                    FIFO
                  </button>

                  <button
                    type="button"
                    className={`scheduler-button ${selectedScheduler === 'SJF' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('SJF')}
                  >
                    SJF
                  </button>

                  <button
                    type="button"
                    className={`scheduler-button ${selectedScheduler === 'RR' ? 'selected' : ''}`}
                    onClick={() => setSelectedScheduler('RR')}
                  >
                    Round Robin
                  </button>

                  <button
                    type="button"
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
      <button onClick={fetchTurnaroundList}>Calcular Turnarounds</button>
      {image && <iframe src={image} width="1200" height="800" title="Process Graph" />}




      {loading && <p>Carregando...</p>}
      {error && <p>{error}</p>}


      {showTurnaroundBox && turnaroundList.length > 0 && (
        <ul turnaround-listclassName="turnaround-list">
          {turnaroundList.map((turnaround, index) => (
            <li key={index} className="turnaround-list-item">{turnaround.name}: {turnaround.value}</li> // Exibe nome e valor
          ))}
        </ul>
      )}

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
