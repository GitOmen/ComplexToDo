import React, {Component} from 'react';
import './App.css';
import Home from './Home';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import TaskList from './TaskList';
import TaskEdit from "./TaskEdit";
import TaskListEdit from "./TaskListEdit";

class App extends Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path='/' exact={true} component={Home}/>
                    <Route path='/tasks' exact={true} component={TaskList}/>
                    <Route path='/lists/new' exact={true} component={TaskListEdit}/>
                    <Route path='/lists/:id' exact={true} component={TaskList}/>
                    <Route path='/lists/:listId/edit' exact={true} component={TaskListEdit}/>
                    <Route path='/tasks/:taskId' exact={true} component={TaskEdit}/>
                    <Route path='/lists/:listId/tasks/:taskId' exact={true} component={TaskEdit}/>
                </Switch>
            </Router>
        )
    }
}

export default App;
