import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8080';

function getTaskTitle(task) {
  return task.title ?? task.text ?? '';
}

function getTaskCompleted(task) {
  return Boolean(task.completed ?? task.is_done ?? false);
}

function getCategoryName(category) {
  return category.name ?? category.title ?? '';
}

function getErrorText(error) {
  const msg = error.response?.data?.detail;
  if (typeof msg === 'string') return msg;
  if (Array.isArray(msg)) return msg.map((item) => item?.msg ?? item).join(', ');
  return 'Request Error';
}

function App() {
  const [activeView, setActiveView] = useState('tasks');

  const [taskTitle, setTaskTitle] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTaskOriginal, setEditingTaskOriginal] = useState(null);
  const [taskStatusMessage, setTaskStatusMessage] = useState('');

  const [categoryName, setCategoryName] = useState('');
  const [categories, setCategories] = useState([]);
  const [editingCategoryId, setEditingCategoryId] = useState(null);
  const [editingCategoryOriginal, setEditingCategoryOriginal] = useState(null);
  const [categoryStatusMessage, setCategoryStatusMessage] = useState('');

  const completedCount = tasks.filter((task) => getTaskCompleted(task)).length;
  const pendingCount = tasks.length - completedCount;

  useEffect(() => {
    fetchTasks();
    fetchCategories();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks`);
      setTasks(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setTaskStatusMessage('Loading Error');
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/categories`);
      setCategories(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setCategoryStatusMessage('categories loading errors');
    }
  };

  const resetTaskForm = () => {
    setTaskTitle('');
    setIsCompleted(false);
    setEditingTaskId(null);
    setEditingTaskOriginal(null);
  };

  const resetCategoryForm = () => {
    setCategoryName('');
    setEditingCategoryId(null);
    setEditingCategoryOriginal(null);
  };

  const handleTaskSubmit = async () => {
    const title = taskTitle.trim();
    if (!title) return;

    try {
      if (editingTaskId) {
        const patchData = {};

        if (!editingTaskOriginal || title !== editingTaskOriginal.title) {
          patchData.title = title;
        }
        if (!editingTaskOriginal || isCompleted !== editingTaskOriginal.completed) {
          patchData.completed = isCompleted;
        }

        if (Object.keys(patchData).length === 0) {
          setTaskStatusMessage('No changes');
          return;
        }

        await axios.patch(`${API_BASE_URL}/tasks/${editingTaskId}`, patchData);
        setTaskStatusMessage('Task was update');
      } else {
        await axios.post(`${API_BASE_URL}/tasks`, { title });
        setTaskStatusMessage('Task was create');
      }

      resetTaskForm();
      fetchTasks();
    } catch (error) {
      console.error('Error submitting task:', error);
      setTaskStatusMessage(`Error: ${getErrorText(error)}`);
    }
  };

  const handleCategorySubmit = async () => {
    const name = categoryName.trim();
    if (!name) return;

    try {
      if (editingCategoryId) {
        const patchData = {};

        if (!editingCategoryOriginal || name !== editingCategoryOriginal.name) {
          patchData.name = name;
        }

        if (Object.keys(patchData).length === 0) {
          setCategoryStatusMessage('No changes');
          return;
        }

        await axios.patch(`${API_BASE_URL}/categories/${editingCategoryId}`, patchData);
        setCategoryStatusMessage('categorie was update');
      } else {
        await axios.post(`${API_BASE_URL}/categories`, { name });
        setCategoryStatusMessage('categorie was create');
      }

      resetCategoryForm();
      fetchCategories();
    } catch (error) {
      console.error('Error submitting category:', error);
      setCategoryStatusMessage(`Error: ${getErrorText(error)}`);
    }
  };

  const handleTaskEdit = (task) => {
    const originalTitle = getTaskTitle(task);
    const originalCompleted = getTaskCompleted(task);

    setTaskTitle(originalTitle);
    setIsCompleted(originalCompleted);
    setEditingTaskId(task.id);
    setEditingTaskOriginal({
      title: originalTitle,
      completed: originalCompleted,
    });
    setTaskStatusMessage('');
  };

  const handleCategoryEdit = (category) => {
    const originalName = getCategoryName(category);

    setCategoryName(originalName);
    setEditingCategoryId(category.id);
    setEditingCategoryOriginal({
      name: originalName,
    });
    setCategoryStatusMessage('');
  };

  const handleToggleCompleted = async (task) => {
    try {
      await axios.patch(`${API_BASE_URL}/tasks/${task.id}`, {
        completed: !getTaskCompleted(task),
      });
      fetchTasks();
    } catch (error) {
      console.error('Error toggling task status:', error);
      setTaskStatusMessage(`Error: ${getErrorText(error)}`);
    }
  };

  const handleTaskDelete = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/tasks/${id}`);
      if (editingTaskId === id) {
        resetTaskForm();
      }
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
      setTaskStatusMessage(`Error: ${getErrorText(error)}`);
    }
  };

  const handleCategoryDelete = async (id) => {
    try {
      await axios.delete(`${API_BASE_URL}/categories/${id}`);
      if (editingCategoryId === id) {
        resetCategoryForm();
      }
      fetchCategories();
    } catch (error) {
      console.error('Error deleting category:', error);
      setCategoryStatusMessage(`Error: ${getErrorText(error)}`);
    }
  };

  return (
    <div className="app-shell">
      <main className="App">
        <header className="hero">
          <div className="hero-head">
            <h1>My tasks</h1>
            <div className="view-switcher" role="tablist" aria-label="Переключатель разделов">
              <button
                className={activeView === 'tasks' ? 'switch-btn active' : 'switch-btn'}
                onClick={() => setActiveView('tasks')}
                type="button"
              >
                Tasks
              </button>
              <button
                className={activeView === 'categories' ? 'switch-btn active' : 'switch-btn'}
                onClick={() => setActiveView('categories')}
                type="button"
              >
                Categories
              </button>
            </div>
          </div>
        </header>

        {activeView === 'tasks' ? (
          <>
            <section className="panel editor-panel">
              <div className="input-row">
                <input
                  type="text"
                  value={taskTitle}
                  onChange={(event) => setTaskTitle(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter') {
                      event.preventDefault();
                      handleTaskSubmit();
                    }
                  }}
                  placeholder="Type Task"
                />
                <button className="btn btn-primary" onClick={handleTaskSubmit} type="button">
                  {editingTaskId ? 'Save' : 'Add'}
                </button>
              </div>

              {editingTaskId && (
                <label className="checkbox-row">
                  <input
                    type="checkbox"
                    checked={isCompleted}
                    onChange={(event) => setIsCompleted(event.target.checked)}
                  />
                  Mark as completed 
                </label>
              )}

              <div className="action-row">
                <button className="btn" onClick={resetTaskForm} type="button">
                  {editingTaskId ? 'Cancel editing' : 'Clear field'}
                </button>
              </div>

              {taskStatusMessage && <div className="status-message">{taskStatusMessage}</div>}
            </section>

            <section className="panel tasks-panel">
              <div className="tasks-header">
                <h2>Task list</h2>
                <button className="btn" onClick={fetchTasks} type="button">
                  Update
                </button>
              </div>

              <div className="stats">
                <span className="stat-pill">Total: {tasks.length}</span>
                <span className="stat-pill">Active: {pendingCount}</span>
                <span className="stat-pill">Completed: {completedCount}</span>
              </div>

              {tasks.length === 0 ? (
                <div className="empty-state">It’s empty for now. Add your first task above.</div>
              ) : (
                <ul>
                  {tasks.map((task, index) => (
                    <li key={task.id} style={{ '--item-index': index }}>
                      <button
                        className={getTaskCompleted(task) ? 'toggle done' : 'toggle'}
                        onClick={() => handleToggleCompleted(task)}
                        aria-label="Toggle status"
                        type="button"
                      >
                        {getTaskCompleted(task) ? '✓' : ''}
                      </button>

                      <div className="task-content">
                        <span className={getTaskCompleted(task) ? 'task-title done' : 'task-title'}>
                          {getTaskTitle(task)}
                        </span>
                        <span className="task-state">{getTaskCompleted(task) ? 'Completed' : 'In progress'}</span>
                      </div>

                      <div className="task-actions">
                        <button className="btn" onClick={() => handleTaskEdit(task)} type="button">
                          Change
                        </button>
                        <button className="btn btn-danger" onClick={() => handleTaskDelete(task.id)} type="button">
                          Delete
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        ) : (
          <>
            <section className="panel editor-panel">
              <div className="input-row">
                <input
                  type="text"
                  value={categoryName}
                  onChange={(event) => setCategoryName(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter') {
                      event.preventDefault();
                      handleCategorySubmit();
                    }
                  }}
                  placeholder="Type Categorie"
                />
                <button className="btn btn-primary" onClick={handleCategorySubmit} type="button">
                  {editingCategoryId ? 'save' : 'add'}
                </button>
              </div>

              <div className="action-row">
                <button className="btn" onClick={resetCategoryForm} type="button">
                  {editingCategoryId ? 'cancel changing' : 'clear field'}
                </button>
              </div>

              {categoryStatusMessage && <div className="status-message">{categoryStatusMessage}</div>}
            </section>

            <section className="panel tasks-panel">
              <div className="tasks-header">
                <h2>Categories List</h2>
                <button className="btn" onClick={fetchCategories} type="button">
                  Update
                </button>
              </div>

              <div className="stats">
                <span className="stat-pill">Total: {categories.length}</span>
              </div>

              {categories.length === 0 ? (
                <div className="empty-state">No categories yet.</div>
              ) : (
                <ul className="category-list">
                  {categories.map((category, index) => (
                    <li key={category.id} style={{ '--item-index': index }}>
                      <div className="category-mark" aria-hidden="true" />

                      <div className="task-content">
                        <span className="task-title">{getCategoryName(category)}</span>
                        <span className="task-state">{category.id}</span>
                      </div>

                      <div className="task-actions">
                        <button className="btn" onClick={() => handleCategoryEdit(category)} type="button">
                          Change
                        </button>
                        <button
                          className="btn btn-danger"
                          onClick={() => handleCategoryDelete(category.id)}
                          type="button"
                        >
                          Delete
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
