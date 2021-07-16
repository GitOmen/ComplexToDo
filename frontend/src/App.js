import './App.css';
import {Component} from "react";

class App extends Component {
  state = {
    tasks: []
  };

  async componentDidMount() {
    const response = await fetch('http://127.0.0.1:5000/tasks');
    const body = await response.json();
    this.setState({tasks: body});
  }

  render() {
    const {tasks} = this.state;
    return (
        <div className="App">
          <header className="App-header">
            <div className="App-intro">
              <h2>Tasks</h2>
              {tasks.map(task =>
                  <div key={task.id}>
                    <hr/>
                    {task.name} ({task.status})
                    <p>
                      {task.description}
                    </p>
                  </div>
              )}
            </div>
          </header>
        </div>
    );
  }
}
export default App;
