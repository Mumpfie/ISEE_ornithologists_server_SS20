package org.example.test;
import org.example.test.api.UserApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Bird;
import org.example.test.model.User;

import java.util.List;

public class Main {
    private static List<User> users;
    private static User user;
    private static Bird bird;

    public static void main(String[] args) {
        UserApi userApi = new UserApi();
        try {
            user = userApi.createUser(new User().name("test"));
        } catch (ApiException e) {
            System.err.println("Api Error");
            System.err.println(e.getResponseBody());
        }
        System.out.println(user != null ? user : "error");
    }
}
