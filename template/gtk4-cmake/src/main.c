#include <gtk/gtk.h>

static int counter = 0;

static void on_button_clicked(GtkWidget *widget, gpointer label)
{
    counter++;

    char label_text[50];
    snprintf(label_text, sizeof(label_text), "%d", counter);
    gtk_label_set_text(GTK_LABEL(label), label_text);

    if (counter >= 10)
    {
        counter = -1;
    }
}

static void on_activate(GtkApplication *app, gpointer user_data)
{
    GtkWidget *window;
    GtkWidget *vbox;
    GtkWidget *label;
    GtkWidget *button;

    // create a window
    window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "GTK4");
    gtk_window_set_default_size(GTK_WINDOW(window), 192, 108);

    vbox = gtk_box_new(GTK_ORIENTATION_VERTICAL, 5);
    gtk_window_set_child(GTK_WINDOW(window), vbox);

    label = gtk_label_new("0");
    gtk_box_append(GTK_BOX(vbox), label);

    // create a button
    button = gtk_button_new_with_label("+1");
    gtk_box_append(GTK_BOX(vbox), button);

    g_signal_connect(button, "clicked", G_CALLBACK(on_button_clicked), label);

    // show the window
    gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char **argv)
{
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
