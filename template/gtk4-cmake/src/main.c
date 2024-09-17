#include <gtk/gtk.h>

static void on_activate(GtkApplication *app, gpointer user_data) {
    GtkWidget *window;
    GtkWidget *button;

    // create a window
    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "GTK4");
    gtk_window_set_default_size(GTK_WINDOW(window), 192, 108);

    // create a button
    button = gtk_button_new_with_label("Hello World");
    gtk_window_set_child(GTK_WINDOW(window), button);

    // show the window
    gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char **argv) {
    GtkApplication *app;
    int status;

    // create application
    app = gtk_application_new("my.gtk", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(on_activate), NULL);

    // start application
    status = g_application_run(G_APPLICATION(app), argc, argv);

    // release
    g_object_unref(app);

    return status;
}
