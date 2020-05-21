package org.example.test;

import io.swagger.annotations.Api;
import org.example.test.api.OccurrenceApi;
import org.example.test.api.UserApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Bird;
import org.example.test.model.Occurrence;
import org.example.test.model.User;

import java.io.File;
import java.time.OffsetDateTime;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        OccurrenceApi occurrenceApi = new OccurrenceApi();
        OffsetDateTime time = OffsetDateTime.now();
        try {
            Occurrence occurrence = occurrenceApi.addOccurrence(new Occurrence().userId(1).birdId(1).latitude(42.0).longitude(42.0).altitude(42.0).note("lol").timestamp(time));
            System.out.println(occurrence);
        } catch (ApiException e) {
            System.err.println(e.getResponseBody());
        }
    }
}
