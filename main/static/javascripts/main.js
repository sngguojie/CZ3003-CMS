$(function () {
	
	$.google = {
		api_key : "AIzaSyAfx3vltb6DmiG9O72T1dni1KweHxVQbNc",
		maps : {
			callback : "$.google.maps.init",
			map : {},
			geocoder : {},
			markers : [],
			load_library : function() {
				var googleMaps = $("<script>", {
					type : "text/javascript",
					src : "http://maps.googleapis.com/maps/api/js?key=" + $.google.api_key + "&region=SG&callback=" + $.google.maps.callback
				}).prop("defer", true).prop("async", true);
				
				$("body").append(googleMaps);
			}, // end $.google.maps.load_library
			init : function() {
				$.google.maps.map = new google.maps.Map(document.getElementById("map"), {
					streetViewControl: false,
					fullscreenControl: false,
					center: {lat: 1.34284, lng: 103.8190145},
					zoom: 11
				});
				$.google.maps.geocoder = new google.maps.Geocoder();
				$.page.update();
			}, // end $.google.maps.init
			marker : {
				icons : {
					Terrorist : {
						icon : "../images/terrorist.svg",
						color : "#FF0000",
						stroke : "#666666"
					},
					Flooding : {
						icon : "../images/flooding.svg",
						color : "#006DF0",
						stroke : "#666666"
					}
				},
				/**
				*	Adds a marker with radius(meters) on Basemap
				*/
				add : function(lat, lng, radius, title, type) {
					var marker = {
						marker : new google.maps.Marker({
							position : {lat:lat, lng:lng},
							map : $.google.maps.map,
							animation: google.maps.Animation.DROP,
							title : title,
							icon : $.google.maps.marker.icons[type].icon
						})
					};
					
					if (radius > 0) {
						marker.circle = new google.maps.Circle({
							strokeColor: $.google.maps.marker.icons[type].stroke,
							strokeOpacity: 0.8,
							strokeWeight: 2,
							fillColor: $.google.maps.marker.icons[type].color,
							fillOpacity: 0.35,
							map: $.google.maps.map,
							center: {lat:lat, lng:lng},
							radius: radius
						});
					}
					
					$.google.maps.markers.push(marker);
				}, // end $.google.maps.marker.add
				clear_all : function() {
					$.google.maps.markers.forEach(function(marker, index) {
						marker.marker.setMap(null);
						if(marker.circle !== undefined) {
							marker.circle.setMap(null);	
						}
					});
					$.google.maps.markers = [];
				} // end $.google.maps.marker.clear_all
			}, // end $.google.maps.marker
			geocode_address : function(address, callback) {
				$.google.maps.geocoder.geocode({
					address : address + ", Singapore",
					region : "SG"
				}, function(results, status) {
					if (status == 'OK') {
						//console.log('Geocoded Result: ', results[0].geometry.location);
						if (callback !== undefined) {
							callback.call(this, results);	
						}
					} else {
						console.log('Geocode was not successful for the following reason: ^', status);
					}
				});
			}, // end $.google.maps.geocode_address
			geocode_latlng : function(location, callback) {
				$.google.maps.geocoder.geocode({
					location : location,
					region : "SG"
				}, function(results, status) {
					if (status == 'OK') {
						console.log('Geocoded Result: ', results);
						if (callback !== undefined) {
							
							callback.call(this, results);	
						}
					} else {
						console.log('Geocode was not successful for the following reason: ^', status);
					}
				});
			} // end $.google.maps.geocode_latlng
		}, // end $.google.maps
		firebase : {
			config : {
				apiKey: "AIzaSyAfx3vltb6DmiG9O72T1dni1KweHxVQbNc",
				serverKey: "AIzaSyDGkaf5JEu3LZmc5_ObZP-7XGqzEhB0vTA",
				//authDomain: "cz3003-cms.firebaseapp.com",
				databaseURL: "https://cz3003-cms.firebaseio.com",
				//storageBucket: "cz3003-cms.appspot.com",
				messagingSenderId: "455786633696"
			}, // end $.google.firebase.config
			messaging : { /* Firebase Messaging Object */ },
			database : { /* Firebase DB Object */ },
			init : function() {
				firebase.initializeApp($.google.firebase.config);
				
				if ('serviceWorker' in navigator) {
					console.log('Service Worker is supported');
					navigator.serviceWorker.register("../javascripts/firebase-messaging-sw.js").then(function(registration) {
						console.log('Service Worker is ready : ^) ', registration);
						
						$.google.firebase.messaging = firebase.messaging();
						$.google.firebase.messaging.useServiceWorker(registration);
						$.google.firebase.token.onrefresh();
						$.google.firebase.receive_message();
						$.google.firebase.token.get();
					}).catch(function(error) {
						console.log('Service Worker error :^(', error);
					});
				}
				
				$.google.firebase.database = firebase.database();
				$.google.firebase.token.db_ref = $.google.firebase.database.ref("push_registrations");
				$.google.firebase.token.db_ref.on('value', function(snapshot) {
					var i = 0;
					$.google.firebase.token.registration_ids = [];
					
					snapshot.forEach(function(row) {
						$.google.firebase.token.registration_ids[i] = row.val().registration_id;
						i++;
					});
				});
				
			}, // end $.google.firebase.init
			token : {
				db_ref : { /* push_registrations firebase database reference */ },
				registration_ids : [ /* list of ids for push messaging */ ],
				onrefresh : function() {
					$.google.firebase.messaging.onTokenRefresh(function() {
						$.google.firebase.messaging.getToken().then(function(refreshedToken) {
							console.log('Token refreshed.');
							// Indicate that the new Instance ID token has not yet been sent to the app server.
							$.google.firebase.token.to_server.is_sent(false);
							// Send Instance ID token to app server.
							$.google.firebase.token.to_server.send(refreshedToken);
						}).catch(function(err) {
							console.log('Unable to retrieve refreshed token ', err);
						});
					});
				}, // end $.google.firebase.token.refresh
				/**
				*	Get Instance ID token. Initially this makes a network call, once retrieved
				*	subsequent calls to getToken will return from cache.
				*/
				get : function() {
					$.google.firebase.messaging.getToken().then(function(currentToken) {
						if (currentToken) {
							console.log(currentToken);
							$.google.firebase.token.to_server.send(currentToken);
							//updateUIForPushEnabled(currentToken);
						} else {
							// Show permission request.
							console.log('No Instance ID token available. Request permission to generate one.');
							// Show permission UI.
							$.google.firebase.request_permission();
							//updateUIForPushPermissionRequired();
							$.google.firebase.token.to_server.is_sent(false);
						}
					}).catch(function(err) {
						console.log('An error occurred while retrieving token. ', err);
						//showToken('Error retrieving Instance ID token. ', err);
						$.google.firebase.token.to_server.is_sent(false);
					});
				}, // end $.google.firebase.token.get
				to_server : {
					send : function(currentToken) {
						if (!$.google.firebase.token.to_server.is_sent()) {
							console.log('Sending token to server...');
							
							$.google.firebase.token.db_ref.push().set({
								registration_id : currentToken,
								groups : $.page.get_cookie("groups"),
								datetime : new Date().getTime()
							}).then(function() {
								console.log('Token has been sent...');
								$.google.firebase.token.to_server.is_sent(true)
							});
						} else {
							console.log('Token already sent to server so won\'t send it again unless it changes');	
						}
					}, // end $.google.firebase.token.to_server.send
					is_sent : function(sent) {
						if (sent === undefined) {
							if (window.localStorage.getItem('sentToServer') == 1) {
								  return true;
							}
							return false;
						} else {
							window.localStorage.setItem('sentToServer', sent ? 1 : 0);
							return sent;
						}
					} // end $.google.firebase.token.to_server.is_sent
				} // end $.google.firebase.token.to_server
			}, // end $.google.firebase.token
			/**
			*	Handle incoming messages. Called when:
			*	- a message is received while the app has focus
			*	- the user clicks on an app notification created by a sevice worker
			*	`messaging.setBackgroundMessageHandler` handler.
			*/
			receive_message : function() {
				$.google.firebase.messaging.onMessage(function(payload) {
					console.log("Message received. ", payload);
					
					var incident = payload.data.incident;
					if(incident !== undefined && incident) {
						$.page.incident.update();
					}
				});
			}, // end $.google.firebase.receive_message
			/**
			*	Callback fired if Instance ID token is updated.
			*/
			request_permission : function() {
				console.log('Requesting permission...');
				$.google.firebase.messaging.requestPermission().then(function() {
					console.log('Notification permission granted.');
					// TODO(developer): Retrieve a Instance ID token for use with FCM.
      				// [START_EXCLUDE]
      				// In many cases once an app has been granted notification permission, it
      				// should update its UI reflecting this.
					$.google.firebase.token.get();
					// [END_EXCLUDE]
				}).catch(function(err) {
					console.log('Unable to get permission to notify. ', err);
				});
			}, // end $.google.firebase.request_permission
			send_broadcast : function(message) {
				var data = {
					"registration_ids" : $.google.firebase.token.registration_ids,
					"data" : message
				};
				
				data = JSON.stringify(data);
				
				$.ajax({
					url : "https://fcm.googleapis.com/fcm/send",
					method : "POST",
					headers : {
						"Content-Type" : "application/json",
						"Authorization" : "key=" + $.google.firebase.config.serverKey
					},
					data : data,
					success: function(data, textStatus, jqXHR) {
						console.log("broadcast sent.. ", data);
					}
				});
			} // end $.google.firebase.send_broadcast
		} // end $.google.firebase
	}
	
	$.page = {
		init : function() {
			var role = $.page.get_cookie("groups");
			
			if (role === "Call_Center") {
				$.page.incident.init(true);
				$("#theme-setting-icon, #theme-setting").remove();
			} else if (role === "PR_Manager") {
				$.page.social_media.init(true);
				$("#theme-setting-icon, #theme-setting").remove();
			} else if (role === "HQ_Commander") {
				$.page.incident.init(true);
				$.page.resource.init();
				$.page.social_media.init();
			} else {
				// back to login
				window.location = "login.html";
			}
			
			$("#skin-1").click(function(e) {
                $.backend.CMS_Status.update(false);
				$("#theme-setting-icon").click();
            });
			
			$("#skin-2").click(function(e) {
                $.backend.CMS_Status.update(true);
				$("#theme-setting-icon").click();
            });
		}, // end $.page.init
		get_cookie : function(c_name) {
			/*var i, x, y, ARRcookies = document.cookie.split(";");
			
			for (i = 0; i < ARRcookies.length; i++) {
				x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
				y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
				x = x.replace(/^\s+|\s+$/g, "");
				if (x == c_name) {
					return unescape(y);
				}
			}*/
			return Cookies.get()[c_name];
		}, // end $.page.get_cookie
		scrollTo : function(element) {
			var height = 0;
			$(element).prevAll().each(function(index, element) {
				height += $(this).outerHeight();
			});
			$("html, body").animate({ scrollTop: height }, 600);
		}, // end $.page.scrollTo
		logout : function() {
			Cookies.remove("groups");
			Cookies.remove("skin_color");
			window.location = "login.html";
		}, // end $.page.logout
		update : function() {
			$.backend.incident.list(function(results) {
				$.page.incident.list = results;
				$.page.incident.update(results);
				$.page.social_media.update(results);
			});
		}, // end $.page.update
		incident : {
			list : [ /* list of retrieved incidents */ ],
			init : function(showView) {
				//load view
				$.ajax({
					url : "incident_management.html",
					success : function(data) {
						var view = $("<div>", {
							id : "incident_view",
							class : "role_view"
						}).appendTo("#main-container");
						
						view.html(data);
						
						if(!showView) view.hide();
						
						$("#incident_create_form").submit($.page.incident.submit_create_form);
					}
				})/*.done(function() {
					$.page.incident.logs.refresh_list();
				})*/;
				
				//load menus
				$.page.incident.menu.init($.page.incident.menu.click);
			}, //end $.page.incident.init
			submit_create_form : function(e) {
				e.preventDefault();
							
				var address = $("#incident-location").val();
				var incident_type = $("#incident-type").val();
				$.google.maps.geocode_address(address, function(results) {
					var location = results[0].geometry.location
					
					//TODO search for existing incidents
					var incident_exists = true;
					$.page.incident.list.forEach(function(incident, index) {
						if (incident.location != null) {
							var incident_location = new google.maps.LatLng(incident.location.coord_lat, incident.location.coord_long)
							
							var dist = google.maps.geometry.spherical.computeDistanceBetween(location, incident_location);
							
							console.log(index, dist);
						}
					});
					
					if (!incident_exists) {
						$.google.maps.geocode_latlng(location, function(results) {
							var address = results[0].formatted_address;
							
							// deactivation_time, activation_time, description, incident_type, radius, coord_lat, coord_long, successCallback
							var coord_lat = location.lat();
							var coord_lng = location.lng();
							var activation_time = new Date();
							$.backend.incident.create(null, activation_time, address, incident_type, 2000, coord_lat, coord_lng, function(id) {
								console.log("created new incident with id : ^", id);
								$.google.firebase.send_broadcast({incident:true});
							});
						});
					}
				});
			}, //end $.page.incident.submit_create_form
			menu : {
				init : function(onClick) {
					$.page.incident.menu.main_menu(onClick);
					$.page.incident.menu.shortcut(onClick);
				},
				main_menu : function(onClick) {
					var li = $("<li>", {
						class : "incident_btn",
						role : "button"
					}).appendTo(".main-menu > ul");
					var a = $("<a>").appendTo(li);
					var icon_wrapper = $("<span>",{
						class : "menu-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-exclamation-triangle fa-lg"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Incident Management").appendTo(a);
					
					li.click(onClick);
				}, //end $.page.incident.menu.main_menu
				shortcut : function(onClick) {
					var a = $("<a>", {
						class : "shortcut-link incident_btn",
						role : "button"
					}).appendTo(".shortcut-wrapper");
					var icon_wrapper = $("<span>",{
						class : "shortcut-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-exclamation-triangle"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Incident Management").appendTo(a);
					
					a.click(onClick);
				}, //end $.page.incident.menu.shortcut
				click : function(e) {
					e.preventDefault();
					
					$(".role_view:not(#incident_view)").slideUp("fast");
					$(".role_view").promise().done(function() {
						$("#incident_view").slideDown("fast");
						$.page.scrollTo("#incident_view");
					});
				}
			}, //end $.page.incident.menu
			get_type_text : function(incident_type) {
				return $("#incident-type option[value=" + incident_type + "]").text();
			}, //end $.page.incident.get_type_text
			update : function(results) {
				$.google.maps.marker.clear_all();
				
				// empty incident table (incident-management)
				var table = $("#incident-table");
				var tbody = table.children("tbody");
				tbody.empty();
				
				results.forEach(function(result, index) {
					//[TODO] remove deactivated incidents?
					if (result.deactivation_time !== null) {
						return;
					}
					
					var location = result.location;
					var description = result.description;
					var type = $.page.incident.get_type_text(result.incident_type);
					
					if (location !== null) {
						var lat = location.coord_lat;
						var lng = location.coord_long;
						var radius = location.radius;
						$.google.maps.marker.add(lat, lng, radius, description, type);
							
						$.google.maps.map.setZoom(11);
						$.google.maps.map.setCenter({lat:lat,lng:lng});
					}
					
					// [START] incident table refresh/update
					var tr = $("<tr>", {
						"data-id" : result.id
					}).css("cursor", "pointer").click(function(e) {
                       $("#incident-log-list").attr({
						    "data-incident-id" : result.id
					   });
					   
					   tbody.children("tr").removeClass("active");
					   $(this).addClass("active");
					   $.page.incident.logs.refresh_list();
                    });
					tr.appendTo(tbody);
					
					$("<td>").text(result.id).appendTo(tr);
					
					var date = "", time = "";
					var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
					if (result.activation_time != null) {
						var datetime = new Date(result.activation_time);
						date = datetime.getDate() + " " + monthNames[datetime.getMonth()] + " " + datetime.getFullYear();
						time = datetime.getHours() + ":" + datetime.getMinutes() + ":" + datetime.getSeconds();
						time = datetime.toTimeString().substr(0, 8);
					}
					$("<td>").text(date + " " + time).appendTo(tr);
					
					$("<td>").text(result.description).appendTo(tr);
					
					var location = "";
					if (result.location !== null) {
						location = result.location.coord_lat + ", " + result.location.coord_long + "; " + result.location.radius + "m";
					}
					$("<td>").text(location).appendTo(tr);
					
					
					$("<td>").text(type).appendTo(tr);
					
					var status = $("<span>");
					$("<td>").append(status).appendTo(tr);
					
					if (result.deactivation_time === null) {
						status.attr("class", "label label-success");
						status.text("ACTIVE");
					} else {
						status.attr("class", "label label-error");
						status.text("CLOSED");
					}
					// [END] incident table refresh/update
				});
				
				tbody.children("tr:last").click();
				table.parent(".incident-table-wrapper").animate({ scrollTop: table.height() }, 100);
			}, //end $.page.incident.update
			logs : {
				refresh_list : function() {
					var incident_id = $("#incident-log-list").attr("data-incident-id");
					if (incident_id === undefined) return;
					$.backend.incident_logs.list(incident_id, function(results){
						//alert(JSON.stringify(results));
						$("#incident-log-list").empty();
						for(var i = 0; i < results.length; i++) {
							var id = results[i].id;
							var description = results[i].description;
							var datetimeString = results[i].datetime;
							
							var list_item = $.page.incident.logs.new_list_item(id, description, datetimeString);
							$("#incident-log-list").prepend(list_item);
						}
					});
				}, // end $.page.incident.logs.refresh_list
				new_list_item : function(id, description, datetimeString) {
					var li = $("<li>", {
						class : "list-group-item clearfix log-item",
						id : id
					});
					
					var icon_wrapper = $("<div>", {
						class : "activity-icon bg-info small"
					}).appendTo(li);
					
					var icon = $("<i>", {
						class : "fa fa-comment"
					}).appendTo(icon_wrapper);
					
					var content_wrapper = $("<div>", {
						class : "pull-left m-left-sm"
					}).appendTo(li);
					
					var text = $("<span>").text(description).appendTo(content_wrapper);
					var br = $("<br>").appendTo(content_wrapper);
					
					var datetime_wrapper = $("<small>", {
						class : "text-muted"	
					}).appendTo(content_wrapper);
					
					var time_icon = $("<i>",{
						class : "fa fa-clock-o"	
					}).appendTo(datetime_wrapper);
					
					datetime_wrapper.append($.page.convert_time_display(datetimeString));
					
					return li;
				},  // end $.page.incident.logs.new_list_item
				create : function(form, e) {
					e.preventDefault();
					
					var incident_id = $("#incident-log-list").attr("data-incident-id");
					if (incident_id === undefined) return;
					
					var description = $("#log-create-description").val();
					if (description.length <= 0) return;
					
					$.backend.incident_logs.create(incident_id, description, function(data) {
						$.page.incident.logs.refresh_list();
						$("#log-create-description").val("");
					});
				}  // end $.page.incident.logs.create
			}  // end $.page.incident.logs
		},  // end $.page.incident
		resource : {
			init : function(showView) {
				//load view
				$.ajax({
					url : "resource_management.html",
					success : function(data) {
						var view = $("<div>", {
							id : "resource_view",
							class : "role_view"
						}).appendTo("#main-container");
						
						view.html(data);
						
						if (!showView) view.hide();
					}
				});
				
				//load controls
				$.page.resource.menu.init($.page.resource.menu.click);
			}, // end $.page.resource.init
			menu : {
				init : function(onClick) {
					$.page.resource.menu.main_menu(onClick);
					$.page.resource.menu.shortcut(onClick);
				}, // end $.page.resource.menu.init
				main_menu : function(onClick) {
					var li = $("<li>", {
						class : "resource_btn",
						role : "button"
					}).appendTo(".main-menu > ul");
					var a = $("<a>").appendTo(li);
					var icon_wrapper = $("<span>",{
						class : "menu-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-users fa-lg"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Resource Management").appendTo(a);
					
					li.click(onClick);
				}, //end $.page.resource.menu.main_menu
				shortcut : function(onClick) {
					var a = $("<a>", {
						class : "shortcut-link resource_btn",
						role : "button"
					}).appendTo(".shortcut-wrapper");
					var icon_wrapper = $("<span>",{
						class : "shortcut-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-user"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Resource Management").appendTo(a);
					
					a.click(onClick);
				}, //end $.page.resource.menu.shortcut
				click : function(e) {
					e.preventDefault();
				
					$(".role_view:not(#resource_view)").slideUp("fast");
					$(".role_view").promise().done(function() {
						$("#resource_view").slideDown("fast");
						$.page.scrollTo("#resource_view");
					});
				}
			}, //end $.page.resource.menu
		}, // end $.page.resource
		social_media : {
			init : function(showView) {
				//load view
				$.ajax({
					url : "media_management.html",
					success : function(data) {
						var view = $("<div>", {
							id : "media_view",
							class : "role_view"
						}).appendTo("#main-container");
						
						view.html(data);
						
						if (!showView) view.hide();
					}
				});
				
				//load controls
				$.page.social_media.menu.init($.page.social_media.menu.click);
			}, // end $.page.social_media.init
			update : function(results) {
				
				// empty timeline
				var timeline = $(".timeline_main");
				timeline.empty();
				
				results.forEach(function(result, index) {
					
					var entry = $("<div>", {
						class : "entry",
						"data-id" : result.id
					}).appendTo(timeline);
					
					var date, time;
					var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
					if (result.activation_time != null) {
						var datetime = new Date(result.activation_time);
						date = datetime.getDate() + " " + monthNames[datetime.getMonth()] + " " + datetime.getFullYear();
						time = datetime.getHours() + ":" + datetime.getMinutes() + ":" + datetime.getSeconds();
						time = datetime.toTimeString().substr(0, 8);
						//date = datetime.toUTCString();
					}
					
					var type = $.page.incident.get_type_text(result.incident_type);
					
					$("<small>").text(date).appendTo(entry);
					$("<h1>").text(time).appendTo(entry);
					$("<h2>").text(type).appendTo(entry);
					$("<div>", {
						style : "overflow:hidden"
					}).text(result.description).appendTo(entry);
					
					timeline.scrollLeft(timeline.width());
				});
			}, // end $.page.social_media.update
			menu : {
				init : function(onClick) {
					$.page.social_media.menu.main_menu(onClick);
					$.page.social_media.menu.shortcut(onClick);
				}, // end $.page.social_media.menu.init
				main_menu : function(onClick) {
					var li = $("<li>", {
						class : "media_btn",
						role : "button"	
					}).appendTo(".main-menu > ul");
					var a = $("<a>").appendTo(li);
					var icon_wrapper = $("<span>",{
						class : "menu-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-envelope-o fa-lg"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Media Management").appendTo(a);
					
					li.click(onClick);
				}, //end $.page.resource.menu.main_menu
				shortcut : function(onClick) {
					var a = $("<a>", {
						class : "shortcut-link media_btn",
						role : "button"
					}).appendTo(".shortcut-wrapper");
					var icon_wrapper = $("<span>",{
						class : "shortcut-icon"
					}).appendTo(a);
					var icon = $("<i>", {
						class : "fa fa-envelope-o"
					}).appendTo(icon_wrapper);
					var text = $("<span>", {
						class : "text"
					}).text("Media Management").appendTo(a);
					
					a.click(onClick);
				}, //end $.page.resource.menu.shortcut
				click : function(e) {
					e.preventDefault();
				
					$(".role_view:not(#media_view)").slideUp("fast");
					$(".role_view").promise().done(function() {
						$("#media_view").slideDown("fast");
						$.page.scrollTo("#media_view");
					});
					
					var timeline = $(".timeline_main");
					$(".timeline_main").scrollLeft(timeline.width());
				}
			} // end $.page.social_media.menu
		}, // end $.page.social_media
		convert_time_display : function(datetimeString) {
			var datetime = new Date(datetimeString);
			var now = new Date();
			
			var diffMillis = now.getTime() - datetime.getTime();
			
			if (diffMillis < 0) diffMillis = 0;
			
			var diffSecs = diffMillis / 1000;
			
			if (diffSecs < 60) {
				var c = Math.ceil(diffSecs);
				if (c > 1) return " " + c + " secs ago";
				else return " " + c + " sec ago";
			}
			
			var diffMins = diffSecs / 60;
			if (diffMins < 60) {
				var c = Math.ceil(diffMins);
				if (c > 1) return " " + c + " mins ago";
				else return " " + c + " min ago";
			}
			
			var diffHrs = diffMins / 60;
			if (diffHrs < 24) {
				var c = Math.ceil(diffHrs);
				if (c > 1) return " " + c + " hrs ago";
				else return " " + c + " hr ago";
			}
			
			var diffDays = diffHrs / 24;
			var c = Math.ceil(diffDays);
			if (c > 1) return " " + c + " days ago";
			else return " " + c + " day ago";
		}  // end $.page.convert_time_display
	} // end $.page
	
	$.backend = {
		//root_url : "https://crisismanagement.herokuapp.com/",
		root_url : "/",
		incident_logs : {
			list : function(incident_id, successCallback) {
				$.ajax({
					url : $.backend.root_url + "Incident/" + incident_id + "/logs/list/",
					method : "GET",
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data.results);	
						}
					}
				});
			}, // end $.backend.incident_logs.list
			create : function(incident_id, description, successCallback) {
				var data = {
					"description" : description
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url + "Incident/" + incident_id + "/logs/create/",
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			} // end $.backend.incident_logs.create
		}, // end $.backend.incident_logs
		incident : {
			list : function(successCallback) {
				$.ajax({
					url : $.backend.root_url + "Incident/list/",
					method : "GET",
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data.results);	
						}
					}
				});
			}, // end $.backend.incident.list
			create : function(deactivation_time, activation_time, description, incident_type, radius, coord_lat, coord_long, successCallback) {
				var data = {
					"deactivation_time" : deactivation_time,
					"activation_time" : activation_time,
					"description" : description,
					"incident_type" : incident_type,
					"location" : {
						"radius" : radius,
						"coord_lat" : coord_lat,
						"coord_long" : coord_long
					}
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url + "Incident/create/",
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data.id);	
						}
					}
				});
			}, // end $.backend.incident.create
			update : function(incident_id, radius, successCallback) {
				var data = {
					"location" : {
						"radius" : radius
					}
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url + "Incident/update/" + incident_id + "/",
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			}, // end $.backend.incident.update
		}, // end $.backend.incident
		call_report : {
			create : function(incident_id, details, successCallback) {
				var data = {
					"incident_id" : incident_id,
					"details" : details
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url,
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			}, // end $.backend.call_report.create
		}, // end $.backend.call_report
		CMS_Status : {
			retrieve : function(successCallback) {
				$.ajax({
					url : $.backend.root_url + "CMSStatus/read/1/",
					method : "GET",
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							if (data.success) {
								successCallback.call(this, data.active);
							}
						}
					}
				});
			}, // end $.backend.CMS_Status.retrieve
			update : function(active, successCallback) {
				var data = {
					"active" : active
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url + "CMSStatus/update/1/",
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			}, // end $.backend.CMS_Status.update
		}, // end $.backend.CMS_Status
		resource : {
			list : function(successCallback) {
				$.ajax({
					url : $.backend.root_url,
					method : "GET",
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			}, // end $.backend.resource.list
			assign : function(to, title, message, successCallback) {
				var data = {
					"to" : to,
					"title" : title,
					"message" : message
				};
				
				// stringify json for backend to recognise
				data = JSON.stringify(data);
				
				$.ajax({
					url : $.backend.root_url + "SMS/create/",
					method : "POST",
					data : data,
					dataType : "json",
					success : function(data, textStatus, jqXHR) {
						if(successCallback !== undefined) {
							successCallback.call(this, data);	
						}
					}
				});
			}, // end $.backend.resource.assign
		} // end $.backend.resource
	} // end $.backend
	
	$(document).ready(function(e) {
        $.google.maps.load_library();
		$.page.init();
		$.google.firebase.init();
    });
});