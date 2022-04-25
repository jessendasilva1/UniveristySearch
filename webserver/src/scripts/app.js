import Navbar from './navbar.js';

import SearchFields from './searchFields.js';
// import Footer from './footer.js';

class App extends React.Component {

	render() {
	  return (
	  		<div id='rootDiv'>
				<Navbar />
				<SearchFields />
				{/*<Footer />*/}
	 		</div>
	  );
	}
  }
ReactDOM.render(<App />, document.getElementById('root'));