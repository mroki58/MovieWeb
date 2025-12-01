import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [

	route("/", "layout.tsx", [
		index("routes/home.tsx")
    ]
	),

	route("/login", "routes/login.tsx"),
	route("/register", "routes/register.tsx"),
	route("/movie/:id", "routes/movie.tsx"),
	route("/actor/:id", "routes/actor.tsx"),
	route("/director/:id", "routes/director.tsx"),
	route("/user/:id", "routes/user.tsx"),
	route("/profile", "routes/profile.tsx"),
] satisfies RouteConfig;
