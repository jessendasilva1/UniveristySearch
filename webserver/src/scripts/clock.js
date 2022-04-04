//import Test from './test.js';
// Display a "Like" <button>

class Clock extends React.Component{

    constructor(props){
        super(props);
        this.state={
            time:0,
            intervalID: 0
        };
        this.clockUpdate = this.clockUpdate.bind(this);
    }

    componentDidMount(){
        var intervalID = setInterval(this.clockUpdate, 1000);
        this.setState({intervalID: intervalID});
    }
/*
    componentWillUnmount(){
        // use intervalId from the state to clear the interval
        clearInterval(this.state.intervalId);
     }
*/
    clockUpdate(){
        this.setState({ time: new Date().toLocaleTimeString() });
    }
    

    render(){
        return (
            <div>
                 <h1>Hello, world!</h1>
                <h2>It is {this.state.time}.</h2>
            </div>
        );
    }
}

export default Clock;

  
  
  