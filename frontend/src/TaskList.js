import React, {Component} from 'react';
import {Button, Container} from 'reactstrap';
import AppNavbar from './AppNavbar';
import {Link} from 'react-router-dom';
import {fetchAllTasks, removeTask} from "./services";
import Task from "./Task";

class TaskList extends Component {

    constructor(props) {
        super(props);
        this.state = {tasks: []};
        this.remove = this.remove.bind(this);
    }

    componentDidMount() {
        fetchAllTasks().then(data => this.setState({tasks: data}));
    }

    async remove(id) {
        await removeTask(id).then(() => {
            let updatedTasks = [...this.state.tasks].filter(i => i.id !== id);
            this.setState({tasks: updatedTasks});
        });
    }

    render() {
        const {tasks, isLoading} = this.state;

        if (isLoading) {
            return <p>Loading...</p>;
        }

        return (
            <div>
                <AppNavbar/>
                <Container>
                    <div className="float-right">
                        <Button color="success" tag={Link} to="/tasks/new">Add Task</Button>
                    </div>
                    <h3>Tasks</h3>
                    {tasks.map(task => <Task task={task} key={task.id}/>)}
                </Container>
            </div>
        );
    }
}

export default TaskList;
