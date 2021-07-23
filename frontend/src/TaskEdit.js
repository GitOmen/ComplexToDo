import React, {Component} from 'react';
import './TaskEdit.css'
import {Link, withRouter} from 'react-router-dom';
import {Button, Container, Form, FormGroup, Input, Label} from 'reactstrap';
import AppNavbar from './AppNavbar';
import TextareaAutosize from 'react-textarea-autosize';
import {createTask, fetchTask, STATUSES, updateTask} from "./services";

class TaskEdit extends Component {

    emptyItem = {
        name: '',
        status: '',
        description: ''
    };

    constructor(props) {
        super(props);
        this.state = {
            item: this.emptyItem
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    async componentDidMount() {
        if (this.props.match.params.id !== 'new') {
            const task = await fetchTask(this.props.match.params.id);
            this.setState({item: task});
        }
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
        if (item.id) {
            await updateTask(item);
        } else {
            await createTask(item);
        }
        this.props.history.push('/tasks');
    }

    render() {
        const {item} = this.state;
        const title = <h2>{item.id ? 'Edit Task' : 'Add Task'}</h2>;

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
                        <Input type="select" name="status" id="status" onChange={this.handleChange}>
                            {Object.entries(STATUSES).map(
                                ([status_value, status_name]) =>
                                    <option
                                        selected={item.status === status_value}
                                        value={status_value}
                                    >{status_name}</option>
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
                        <Button color="secondary" tag={Link} to="/tasks">Cancel</Button>
                    </FormGroup>
                </Form>
            </Container>
        </div>
    }
}

export default withRouter(TaskEdit);
