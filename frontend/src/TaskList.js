import React, {Component} from 'react';
import {Button, Container} from 'reactstrap';
import AppNavbar from './AppNavbar';
import {Link} from 'react-router-dom';
import {fetchAllTasks, fetchTaskList, fetchTaskListTasks, removeTask, removeTaskList} from "./services";
import Task from "./Task";

class TaskList extends Component {

    constructor(props) {
        super(props);
        this.state = {tasks: []};
        this.remove = this.remove.bind(this);
    }

    componentDidMount() {
        if (this.props.match.params.id) {
            fetchTaskListTasks(this.props.match.params.id).then(data => this.setState({tasks: data}));
            fetchTaskList(this.props.match.params.id).then(data => this.setState({list: data}));
        } else {
            fetchAllTasks().then(data => this.setState({tasks: data}));
        }
    }


    async remove(id) {
        await removeTask(id).then(() => {
            let updatedTasks = [...this.state.tasks].filter(i => i.id !== id);
            this.setState({tasks: updatedTasks});
        });
    }

    async removeTaskList(id) {
        await removeTaskList(id);
        this.props.history.push('/');
    }


    render() {
        const {list, tasks, isLoading} = this.state;
        if (isLoading) {
            return <p>Loading...</p>;
        }

        return (
            <div>
                <AppNavbar/>
                <Container>
                    <div className="float-right">
                        <Button
                            color="success" tag={Link} to={(list ? `/lists/${list.id}` : '') + "/tasks/new"}>Add Task
                        </Button>
                    </div>
                    <h3>{list ? list.name : "All Tasks"}</h3>
                    {list ? <>
                        <Button outline color="primary" tag={Link} to={`/lists/${list.id}/edit`}>Edit</Button>
                        <Button size="sm" color="danger" onClick={() => this.removeTaskList(list.id)}>Delete</Button>
                    </> : null}
                    {tasks.map(task => <Task task={task} key={task.id} listId={list ? list.id : null}
                                             onRemove={this.remove}/>)}
                </Container>
            </div>
        );
    }
}

export default TaskList;
