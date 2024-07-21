import React, { useState,useEffect } from 'react';
import axios from 'axios';

function App() {
  const [processList, setProcessList] = useState([]);
  const [image, setImage] = useState('');
  const [newProcess, setNewProcess] = useState({
    tempo_chegada: '',
    tempo_execucao: '',
    deadline: '',
    quantum_sistema: '',
    sobrecarga_sistema: '',
    paginas: ''
  });
  
  useEffect(() => {
    // Busca a lista de processos do backend quando o componente é montado
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

    // Converte o campo 'paginas' de string para array de números
    const processData = {
      ...newProcess,
      paginas: newProcess.paginas.split(',').map(Number)
    };

    axios.post('http://localhost:8000/newprocess', processData)
      .then(response => {
        // Atualiza o estado com a lista de processos recebida
        setProcessList(response.data.process);
        // Limpa o formulário
        setNewProcess({
          tempo_chegada: '',
          tempo_execucao: '',
          deadline: '',
          tempo_restante: '',
          quantum_sistema: '',
          sobrecarga_sistema: '',
          paginas: ''
        });
      })
      .catch(error => {
        console.error('There was an error adding the process!', error);
      });
  };

  const createGraph = () => {
    axios.post('http://localhost:8000/creategraph')
      .then(response => {
        // Atualiza o estado com a imagem recebida
        setImage(`data:image/png;base64,${response.data.image}`);
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
        {processList.length === 0 && (
        <>
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
                value={newProcess.sobrecarga_sistema }
                onChange={handleChange}
                required
              />
            </label>
          </div>
        </>
      )}
      {/* <div>
          <label>Tempo restante:
            <input
              type="number"
              name="tempo_restante"
              value={newProcess.tempo_restante}
              onChange={handleChange}
              required
            />
          </label>
        </div>*/}
        <div>
          <label>Páginas (separadas por vírgula):
            <input
              type="text"
              name="paginas"
              value={newProcess.paginas}
              onChange={handleChange}
              required
            />
          </label>
        </div>
        <button type="submit">Add Process</button>
      </form>

      <button onClick={createGraph}>Create Graph</button>
      {image && <img src={image} alt="Process Graph" />}
      
      <div>
        <h2>Process List</h2>
        <ul>
          {processList.map((process) => (
            <li key={process.id}>
              ID: {process.id}, Tempo Chegada: {process.tempo_chegada}, Tempo Execução: {process.tempo_execucao}, Deadline: {process.deadline}, Sobrecarga:{process.sobrecarga_sistema}, Quantum:{process.quantum_sistema}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
