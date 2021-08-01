import React, {Component} from 'react';
import './TaskEdit.css'
import {Link, withRouter} from 'react-router-dom';
import {Button, Container, Form, FormGroup, Input, Label} from 'reactstrap';
import AppNavbar from './AppNavbar';
import TextareaAutosize from 'react-textarea-autosize';
import {createTask, DEFAULT_STATUS, fetchAllTaskLists, fetchTask, STATUSES, updateTask} from "./services";

class TaskEdit extends Component {

    constructor(props) {
        super(props);
        this.state = {
            item: {
                name: '',
                status: DEFAULT_STATUS,
                description: '',
                list_id: this.props.match.params.listId,
            },
            lists: []
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    async componentDidMount() {
        if (this.props.match.params.taskId !== 'new') {
            const task = await fetchTask(this.props.match.params.taskId);
            const item = {
                id: task.id,
                name: task.name,
                status: task.status,
                list_id: task.list.id,
                description: task.description
            }
            this.setState({item});
        }
        this.setState({lists: await fetchAllTaskLists()})
    }

    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        let item = {...this.state.item};
        item[name] = value;
        this.setState({item});
    }

    async handleSubmit(event) {
        event.preventDefault();
        const {item} = this.state;
        if (!item.list_id) {
            return;
        }
        if (item.id) {
            await updateTask(item);
        } else {
            await createTask(item);
        }
        if (this.props.match.params.listId) {
            this.props.history.push(`/lists/${this.props.match.params.listId}`);
        } else {
            this.props.history.push('/tasks');
        }
    }

    render() {
        const {item, lists} = this.state;
        const title = <h2>{item.id ? 'Edit Task' : 'Add Task'}</h2>;
        const listId = this.props.match.params.listId;

        return <div>
            <AppNavbar/>
            <Container>
                {title}
                <Form onSubmit={this.handleSubmit}>
                    <FormGroup>
                        <Label for="name">Name</Label>
                        <Input type="text" name="name" id="name" value={item.name || ''}
                               onChange={this.handleChange}/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="status">Status</Label>
                        <Input type="select" name="status" id="status" value={item.status}
                               onChange={this.handleChange}>
                            {Object.entries(STATUSES).map(
                                ([status_value, status_name]) =>
                                    <option value={status_value} key={status_value}>{status_name}</option>
                            )}
                        </Input>
                    </FormGroup>
                    <FormGroup>
                        <Label for="list_id">List</Label>
                        <Input type="select" name="list_id" id="list_id" value={item.list_id || ''}
                               onChange={this.handleChange}>
                            <option value={''} hidden/>
                            {lists.map((task_list) =>
                                <option value={task_list.id} key={task_list.id}>{task_list.name}</option>
                            )}
                        </Input>
                    </FormGroup>
                    <FormGroup>
                        <Label for="description">Description</Label>
                        <TextareaAutosize name="description" id="description" value={item.description || ''}
                                          onChange={this.handleChange}/>
                    </FormGroup>
                    <FormGroup>
                        <Button color="primary" type="submit">Save</Button>{' '}
                        <Button color="secondary" tag={Link} to={listId ? `/lists/${listId}` : "/tasks"}>Cancel</Button>
                    </FormGroup>
                </Form>
            </Container>
        </div>
    }
}

export default withRouter(TaskEdit);
