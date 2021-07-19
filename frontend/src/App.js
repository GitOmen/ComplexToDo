import React, { Component } from 'react';
import './App.css';
import Home from './Home';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import TaskList from './TaskList';
import TaskEdit from "./TaskEdit";

class App extends Component {
  render() {
    return (
        <Router>
          <Switch>
            <Route path='/' exact={true} component={Home}/>
            <Route path='/tasks' exact={true} component={TaskList}/>
            <Route path='/tasks/:id' component={TaskEdit}/>
          </Switch>
        </Router>
    )
  }
}

export default App;
