//'use strict';

class LikeButton extends React.Component {
	constructor(props) {
    		super(props);
    		this.state = { liked: false };
  	}

  	render() {
    		if (this.state.liked) {
      			return(
					<button 
						type="button" 
						onClick={() => this.setState({ liked: false})}
						className={"btn btn-success likeButton"}
						>
						You liked this
					</button>
				);
			}

		return (
			<button 
				type="button" 
				onClick={() => this.setState({ liked: true})}
				className={"btn btn-info likeButton"}
				>
				Like
			</button>
		);
	};	
}

export default LikeButton;