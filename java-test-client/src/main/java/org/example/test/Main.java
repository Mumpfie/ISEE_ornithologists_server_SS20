package org.example.test;

import org.example.test.api.UserApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Bird;
import org.example.test.model.User;

import java.io.File;
import java.util.List;

public class Main {
    private static List<User> users;
    private static User user;
    private static Bird bird;
    private static ClassLoader classLoader = Main.class.getClassLoader();
    private static File picture = new File(classLoader.getResource("daten.png").getFile());

    public static void main(String[] args) {
        UserApi userApi = new UserApi();
        System.out.println(picture.isFile());
        try {
            user = userApi.getUsers("test2", 0, 0).get(0);
            //user = userApi.updateUser(user.getId(), user.name("test2"));
            userApi.addPictureToUser(user.getId(),picture);
        } catch (ApiException e) {
            System.err.println("Api Error");
            System.err.println(e.getResponseBody());
        }
        System.out.println(user);
    }
}
