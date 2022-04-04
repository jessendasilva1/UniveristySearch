class JqueryExample extends React.Component {
    constructor(props) {
        super(props);
            this.state = {
                name: "React",
                jqueryMessage: ''
            };
	  
        this.jqueryTest = this.jqueryTest.bind(this);
    }

    jqueryTest(){
        $.ajax({ 
            type: 'GET', 
            url: "https://catfact.ninja/fact", 
            success: (result) =>{
                this.setState({ jqueryMessage: result});
                console.log("URL: https://catfact.ninja/fact, Response: ", this.state.jqueryMessage.fact);
        }});
    };


    render() {
      return (
        <div id='jqueryDiv'>
			<button className='jqueryButton btn btn-info' onClick={this.jqueryTest}>Get a Random Cat Fact</button>
            <span>{this.state.jqueryMessage.fact}</span>
        </div>
      );
    }
  }
//ReactDOM.render(<NewRadio /> , document.getElementById('newRadio'));

export default JqueryExample;