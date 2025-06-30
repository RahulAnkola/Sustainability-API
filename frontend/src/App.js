import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [actions, setActions] = useState([]);
  const [form, setForm] = useState({ action: '', date: '', points: '' });

  const API_URL = 'http://127.0.0.1:8000/api/actions/';

  useEffect(() => {
    fetchActions();
  }, []);

  const fetchActions = () => {
    axios.get(API_URL).then(res => {
      setActions(res.data);
    });
  };

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    axios.post(API_URL, form).then(() => {
      setForm({ action: '', date: '', points: '' });
      fetchActions();
    });
  };

  const handleDelete = id => {
    axios.delete(`${API_URL}${id}/`).then(() => {
      fetchActions();
    });
  };

  const handleUpdate = id => {
    
    if (!form.action || !form.date || !form.points) {
      alert("Please fill in all form fields before updating.");
      return;
    }

    const updated = { ...form, id: id };
    axios.put(`${API_URL}${id}/`, updated).then(() => {
      setForm({ action: '', date: '', points: '' });
      fetchActions();
    });
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Sustainability Actions</h2>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="action"
          placeholder="Action"
          value={form.action}
          onChange={handleChange}
        />
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
        />
        <input
          type="number"
          name="points"
          placeholder="Points"
          value={form.points}
          onChange={handleChange}
        />
        <button type="submit">Add</button>
      </form>

      <table border="1" cellPadding="5" style={{ marginTop: '20px' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Action</th>
            <th>Date</th>
            <th>Points</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {actions.map(a => (
            <tr key={a.id}>
              <td>{a.id}</td>
              <td>{a.action}</td>
              <td>{a.date}</td>
              <td>{a.points}</td>
              <td>
                <button onClick={() => handleUpdate(a.id)}>Update</button>
                <button onClick={() => handleDelete(a.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
