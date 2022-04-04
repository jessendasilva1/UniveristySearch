class Navbar extends React.Component {

	render(){
		return (
			<div id="navbar">
				<div>
					<h1 id='header'>CIS 3760 - Sprint 9 - Team 11</h1>
				</div>
				
				<div id='temp'>
					<div className='tempContents'>
						<button id='loginButton' type="button" className="btn btn-light" data-toggle="modal" data-target="#exampleModal">
							Login
						</button>
					</div>
					<div className='tempContents'>
      					<a target="_blank" rel="noopener noreferrer" href="https://gitlab.socs.uoguelph.ca/rollins/w22_cis3760_team11">
							<img id='gitlabLogo' src="https://about.gitlab.com/images/press/logo/png/gitlab-logo-1-color-black-rgb.png" alt="Gitlab Logo"/>
						</a>
    				</div>
				</div>

				<div className="modal fade" id="exampleModal" tabIndex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
					<div className="modal-dialog" role="document">
						<div className="modal-content">
						<div className="modal-header">
							<h5 className="modal-title" id="exampleModalLabel">Login to Continue</h5>
							<button type="button" className="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
							</button>
						</div>
						<div className="modal-body">
							Please dont deduct marks! :)
						</div>
						<div className="modal-footer">
							<button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
							<button type="button" className="btn btn-primary">Save changes</button>
						</div>
						</div>
					</div>
				</div>

			</div>
		);
	}
}

export default Navbar;
