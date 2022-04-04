const darkClass = `btn btn-dark btnExample`

class Buttons extends React.Component {
  render(){
    return(
      <div id='bootstrapExample'>
        <button type="button" className="btn btn-primary btnExample">Primary</button>
        <button type="button" className="btn btn-secondary btnExample">Secondary</button>
        <button type="button" className="btn btn-success btnExample">Success</button>
        <button type="button" className="btn btn-danger btnExample">Danger</button>
        <button type="button" className="btn btn-warning btnExample">Warning</button>
        <button type="button" className="btn btn-info btnExample">Info</button>
        <button type="button" className="btn btn-light btnExample">Light</button>
        <button type="button" className={darkClass}>Dark</button>
      </div>
    );
  }
}

//ReactDOM.render(<Buttons />, document.getElementById('buttons'));

export default Buttons;